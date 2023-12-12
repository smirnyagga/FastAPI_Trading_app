import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationRead, OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["operation"],
)


@router.get('', response_model=list[OperationRead])
async def get_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        # statement(stmt)=запрос на удаление или вставку. query- выборка
        result = await session.execute(query)
        return result.all()
    except:
        # передать разработчикакм, поместить в БД, когда ошибка неожиданная
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('')
async def add_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}


@router.get('/long_operation')
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return 'много данных'
