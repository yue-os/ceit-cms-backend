from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleWithAuthor
from app.schemas.auth import TokenData
from app.services import article_service
from app.api.v1.dependencies import get_current_user


router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_in: ArticleCreate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await article_service.create_article(db, article_in, current_user.sub)


@router.get("/", response_model=List[ArticleWithAuthor])
async def get_all_articles(
    db: AsyncSession = Depends(get_db)
):
    return await article_service.get_all_articles(db)


@router.get("/my-articles", response_model=List[ArticleWithAuthor])
async def get_my_articles(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await article_service.get_my_articles(db, current_user.sub)


@router.get("/{article_id}", response_model=ArticleWithAuthor)
async def get_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await article_service.get_article(db, article_id)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: UUID,
    article_in: ArticleUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await article_service.update_article(db, article_id, article_in, current_user.sub)


@router.delete("/{article_id}", status_code=status.HTTP_200_OK)
async def delete_article(
    article_id: UUID,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await article_service.delete_article(db, article_id, current_user.sub)
