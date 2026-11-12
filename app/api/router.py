from fastapi import APIRouter

from app.api.routes import auth, categories, health, inventory, products, roles, slides, storefront_settings, uploads
from app.api.routes.admin_resources import payments_router, settings_router, users_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(slides.router)
api_router.include_router(categories.router)
api_router.include_router(uploads.router)
api_router.include_router(storefront_settings.router)
api_router.include_router(inventory.router)
api_router.include_router(payments_router)
api_router.include_router(users_router)
api_router.include_router(roles.router)
api_router.include_router(settings_router)
