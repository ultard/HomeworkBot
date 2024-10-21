from aiogram import Router

from app.routers.settings import settings_router
from app.routers.start import start_router
from app.routers.invoice import invoices_router
from app.routers.tasks import tasks_router

router = Router()
router.include_routers(
    start_router,
    tasks_router,
    invoices_router,
    settings_router
)