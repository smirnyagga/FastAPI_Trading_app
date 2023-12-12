from fastapi import APIRouter, Depends, BackgroundTasks

from ..auth.base_config import current_user

from .tasks import send_email_report_dashboard

router = APIRouter(prefix='/report')


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        'status': 'success',
        'data': 'письмо отправлено',
        'details': None
    }

# альтернатива. с помощью бэкграунда
# @router.get("/dashboard")
# def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
#     background_tasks.add_task(send_email_report_dashboard, user.username)
#     return {
#         "status": 200,
#         "data": "Письмо отправлено",
#         "details": None
#     }

# синхронно
# @router.get("/dashboard")
# def get_dashboard_report(user=Depends(current_user)):
#     # 1400 ms - Клиент ждет
#     send_email_report_dashboard(user.username)
#     return {
#         "status": 200,
#         "data": "Письмо отправлено",
#         "details": None}