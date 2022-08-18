from rest_framework.serializers import ModelSerializer
from .models import (
    SchedulePlan, StructuralDivision, Account, PlannedAmount,
    PerformanceIndicator, PreviusYearFact, Category, Branch
)


class SchedulePlanSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = SchedulePlan
        

class StructuralDivisionSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = StructuralDivision


class AccountSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Account


class PlannedAmountSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = PlannedAmount


class PerformanceIndicatorSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = PerformanceIndicator
        

class PreviusYearFactSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = PreviusYearFact          


class CategorySerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Category  


class BranchSerializer(ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Branch  
