from fastapi import APIRouter

from . import auth
from .application_items import router as application_items_router
from .applications import router as applications_router
from .contracts import router as contracts_router
from .employees import router as employees_router
from .org_units import router as org_units_router
from .organizations import router as organizations_router
from .providers import router as providers_router
from .roles import router as roles_router
from .trainers import router as trainers_router
from .training_courses import router as training_courses_router
from .training_participants import router as training_participants_router
from .training_sessions import router as training_sessions_router
from .user_roles import router as user_roles_router
from .users import router as users_router

router = APIRouter()


router.include_router(application_items_router)
router.include_router(applications_router)
router.include_router(auth.router)
router.include_router(contracts_router)
router.include_router(employees_router)
router.include_router(org_units_router)
router.include_router(organizations_router)
router.include_router(providers_router)
router.include_router(roles_router)
router.include_router(trainers_router)
router.include_router(training_courses_router)
router.include_router(training_participants_router)
router.include_router(training_sessions_router)
router.include_router(user_roles_router)
router.include_router(users_router)