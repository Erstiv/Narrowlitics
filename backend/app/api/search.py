import time

from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import Scene, SearchHistory
from app.schemas.schemas import SearchRequest, SceneOut

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=list[SceneOut])
async def search_scenes(body: SearchRequest, db: AsyncSession = Depends(get_db)):
    """Hybrid search: SQL filters for now, vector search added in Phase 2."""
    start = time.time()

    query = select(Scene).where(Scene.overall_confidence >= body.min_confidence)

    # Character filter
    if body.characters:
        for char in body.characters:
            query = query.where(
                Scene.characters_present.cast(text("text")).ilike(f"%{char}%")
            )

    # Text search on dialog and descriptions
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

    latency = (time.time() - start) * 1000

    # Log search
    db.add(SearchHistory(query=body.query, result_count=len(scenes), latency_ms=latency))
    await db.commit()

    return scenes
