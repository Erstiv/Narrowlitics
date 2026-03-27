import time
import logging

from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.embeddings import embed_query
from app.models.models import Scene, SearchHistory
from app.schemas.schemas import SearchRequest, SearchResult, SceneOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=list[SearchResult])
async def search_scenes(body: SearchRequest, db: AsyncSession = Depends(get_db)):
    """Hybrid search: vector similarity + SQL filters.

    Strategy:
    1. Embed the query text via Gemini text-embedding-004
    2. Find scenes by cosine similarity (pgvector)
    3. Apply SQL filters (characters, min_confidence) on top
    4. Return ranked results with similarity scores
    """
    start = time.time()

    try:
        query_embedding = await embed_query(body.query)
    except Exception as e:
        logger.warning(f"Embedding failed, falling back to text search: {e}")
        query_embedding = None

    if query_embedding is not None:
        # Vector similarity search using pgvector cosine distance
        # 1 - cosine_distance = cosine_similarity (0 to 1)
        similarity_expr = (
            1 - Scene.description_embedding.cosine_distance(query_embedding)
        )

        query = (
            select(Scene, similarity_expr.label("similarity"))
            .where(Scene.description_embedding.isnot(None))
            .where(Scene.overall_confidence >= body.min_confidence)
        )

        # Character filter
        if body.characters:
            for char in body.characters:
                query = query.where(
                    Scene.characters_present.cast(text("text")).ilike(f"%{char}%")
                )

        query = query.order_by(similarity_expr.desc()).limit(body.limit)
        result = await db.execute(query)
        rows = result.all()

        results = [
            SearchResult(
                scene=SceneOut.model_validate(row[0]),
                similarity=round(float(row[1]), 4),
            )
            for row in rows
        ]
    else:
        # Fallback: text-based search (no embeddings available)
        query = select(Scene).where(Scene.overall_confidence >= body.min_confidence)

        if body.characters:
            for char in body.characters:
                query = query.where(
                    Scene.characters_present.cast(text("text")).ilike(f"%{char}%")
                )

        if body.query:
            like_pattern = f"%{body.query}%"
            query = query.where(
                Scene.key_dialog.cast(text("text")).ilike(like_pattern)
                | Scene.description_text.ilike(like_pattern)
                | Scene.actions.ilike(like_pattern)
            )

        query = query.order_by(Scene.overall_confidence.desc()).limit(body.limit)
        result = await db.execute(query)
        scenes = result.scalars().all()

        results = [
            SearchResult(
                scene=SceneOut.model_validate(scene),
                similarity=0.0,
            )
            for scene in scenes
        ]

    latency = (time.time() - start) * 1000

    # Log search analytics
    db.add(SearchHistory(
        query=body.query,
        result_count=len(results),
        latency_ms=latency,
    ))
    await db.commit()

    logger.info(f"Search '{body.query}': {len(results)} results in {latency:.0f}ms")
    return results
