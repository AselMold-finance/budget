from rest_framework.routers import SimpleRouter
from .views import (
    SchedulePlanApiView, StructuralDivisionApiView, AccountApiView, PlannedAmountApiView,
    PerformanceIndicatorApiView, PreviusYearFactApiView, CategoryApiView, BranchApiView
)

router = SimpleRouter()

router.register('shedule-plan', SchedulePlanApiView)
router.register('structual-division', StructuralDivisionApiView)
router.register('account', AccountApiView)
router.register('planned-amount', PlannedAmountApiView)
router.register('perfomance-indicator', PerformanceIndicatorApiView)
router.register('previus-year', PreviusYearFactApiView)
router.register('category', CategoryApiView)
router.register('branch', BranchApiView)


urlpatterns = [
] + router.urls
