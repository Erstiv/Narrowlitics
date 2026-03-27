from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import Episode, Show
from app.schemas.schemas import EpisodeOut, EpisodeStatusUpdate

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.get("/", response_model=list[EpisodeOut])
async def list_episodes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Episode).order_by(Episode.season, Episode.episode_number))
    return result.scalars().all()


@router.get("/{episode_id}", response_model=EpisodeOut)
async def get_episode(episode_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Episode).where(Episode.id == episode_id))
    episode = result.scalar_one_or_none()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode


@router.patch("/{episode_id}/status", response_model=EpisodeOut)
async def update_episode_status(
    episode_id: int, body: EpisodeStatusUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Episode).where(Episode.id == episode_id))
    episode = result.scalar_one_or_none()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    episode.status = body.status
    await db.commit()
    await db.refresh(episode)
    return episode
