from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import House, HouseVI, HouseResponse, CompetitionResponse, Response, Competition
from typing import List
from typing import Annotated, Any
from ..database import async_get_db
from fastapi import APIRouter, Depends, Request
router = APIRouter(tags=["search"])
from sqlalchemy import desc, func, select, or_
from fastapi import HTTPException, status
from typing import Literal

# from sqlalchemy.future import select


async def search_houses(db: AsyncSession, keyword: str = None):
    if keyword is None:
        # Get the 6 most recent houses if keyword is None
        query = select(House).order_by(desc(House.formatted_date)).limit(6)
    else:
        query = select(House).where(
            or_(
                House.motion.ilike(f'%{keyword}%'),
                House.topic_name.ilike(f'%{keyword}%'),
                House.post_type.ilike(f'%{keyword}%'),
                House.describe.ilike(f'%{keyword}%'),
            )
        ).limit(6)

     

    result = await db.execute(query)
    return result.scalars().all()

async def search_competition(db: AsyncSession, keyword: str = None):
    if keyword is None:
        # Get the 6 most recent houses if keyword is None
        query = select(Competition).order_by(desc(Competition.date)).limit(6)
    else:
        query = select(Competition).where(
            or_(
                Competition.motion.ilike(f'%{keyword}%'),
                Competition.infoslide.ilike(f'%{keyword}%'),
                Competition.country.ilike(f'%{keyword}%'),
                Competition.city.ilike(f'%{keyword}%'),
                Competition.level.ilike(f'%{keyword}%'),
                Competition.region.ilike(f'%{keyword}%'),
                Competition.round.ilike(f'%{keyword}%'),
            )
        ).limit(6)

    result = await db.execute(query)
    return result.scalars().all()



async def search_houses_vi(db: AsyncSession, keyword: str = None):
    if keyword is None:
        # Get the 6 most recent houses if keyword is None
        query = select(HouseVI).order_by(desc(HouseVI.formatted_date)).limit(6)
    else:
        # Using %keyword% for a wildcard search with a limit of 6
        query = select(HouseVI).where(
            or_(
                HouseVI.motion.ilike(f'%{keyword}%'),
                HouseVI.topic_name.ilike(f'%{keyword}%'),
                HouseVI.post_type.ilike(f'%{keyword}%'),
                HouseVI.describe.ilike(f'%{keyword}%'),
            )
        ).limit(6)

        # Use `ilike` with unnest to search through array fields
       

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/search", response_model=List[Response], response_model_exclude_none=True)
async def get_users(search: str= None, 
                    lang: Literal["en", "vi"] = "vi",  
                    type_data: Literal["house", "competition"] = "house",
                    db: AsyncSession = Depends(async_get_db)):
    if lang == "en" and type_data =="house":
        houses = await search_houses(db, search)
    else:
        if lang == "vi" and type_data=="house":
            houses = await search_houses_vi(db, search)
        else: 
            if type_data == "competition":
                houses = await search_competition(db, search)
    if not houses:
        return []
    else:
        return [
            Response(
                motion=house.motion,
                id=house.id,
            )
            for house in houses
        ]

async def get_house_by_id(db: AsyncSession, house_id: int):
    # Query the House by id
    result = await db.execute(select(House).where(House.id == house_id))
    house = result.scalar_one_or_none()

    if house is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="House not found"
        )
    
    return house

async def get_house_vi_by_id(db: AsyncSession, house_id: int):
    # Query the House by id
    result = await db.execute(select(HouseVI).where(HouseVI.id == house_id))
    house = result.scalar_one_or_none()

    if house is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="House not found"
        )
    
    return house


@router.get("/search/house/{_id}", response_model=HouseResponse, response_model_exclude_none=True)
async def get_users(_id: int, lang: str = "en", type: str = "en", db: AsyncSession = Depends(async_get_db)):
    if lang == "en":
        house = await get_house_by_id(db, _id)
    else:
        house = await get_house_by_id(db, _id)
    return HouseResponse(
            motion=house.motion,
            topic_name=house.topic_name,
            post_type=house.post_type,
            describe=house.describe,
            points_for=house.points_for or [],  # Đảm bảo là danh sách
            points_again=house.points_against or [],  # Đảm bảo là danh sách
            bibliography=house.bibliography or [],  # Đảm bảo là danh sách
            formatted_date=house.formatted_date  # Có thể là None
        )
@router.get("/search/competition/{_id}", response_model=CompetitionResponse, response_model_exclude_none=True)
async def get_users(_id: int, lang: str = "en", type: str = "en", db: AsyncSession = Depends(async_get_db)):
    result = await db.execute(select(Competition).where(Competition.id == _id))
    house = result.scalar_one_or_none()

    if house is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competition not found"
        )
    
    return CompetitionResponse(
            id= house.id,
            motion=house.motion,
            city=house.city,
            country =house.country,
            infoslide =house.infoslide,
            level =house.level,
            region=house.region,
            round =house.round,
            tournament =house.tournament,
            types =house.types or [], 
        )