from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.operations.router import get_operations

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)


templates = Jinja2Templates(directory='src/templates')    # 'src/templates' относительно майна

@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/search/{operation_type}')   # если в функции, которую используем в депендс требуется аргумент принять- его обязательно в путь
def get_search_page(request: Request, operations=Depends(get_operations)):
    return templates.TemplateResponse('search.html', {'request': request, 'operations': operations})


@router.get('/chat')
def get_chat(request: Request):
    return templates.TemplateResponse('chat.html', {'request': request})
