from rest_framework.viewsets import ModelViewSet
from .serializers import (
    SchedulePlanSerializer, StructuralDivisionSerializer, AccountSerializer, PlannedAmountSerializer,
    PerformanceIndicatorSerializer, PreviusYearFactSerializer, CategorySerializer, BranchSerializer
)
from .models import (
    SchedulePlan, StructuralDivision, Account, PlannedAmount,
    PerformanceIndicator, PreviusYearFact, Category, Branch
)
# Create your views here.


class SchedulePlanApiView(ModelViewSet):
    
    queryset = SchedulePlan.objects.all()
    serializer_class = SchedulePlanSerializer


class StructuralDivisionApiView(ModelViewSet):
    
    queryset = StructuralDivision.objects.all()
    serializer_class = StructuralDivisionSerializer
    

class AccountApiView(ModelViewSet):
    
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    

class PlannedAmountApiView(ModelViewSet):
    
    queryset = PlannedAmount.objects.all()
    serializer_class = PlannedAmountSerializer
    

class PerformanceIndicatorApiView(ModelViewSet):
    
    queryset = PerformanceIndicator.objects.all()
    serializer_class = PerformanceIndicatorSerializer
    

class PreviusYearFactApiView(ModelViewSet):
    
    queryset = PreviusYearFact.objects.all()
    serializer_class = PreviusYearFactSerializer


class BranchApiView(ModelViewSet):
    
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CategoryApiView(ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
