from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *



class AccountInline(admin.TabularInline):
    model = Account


class BranchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('branch_number', 'status', 'user', 'is_structual')
    date_hierarchy = 'create_date'
    list_filter = ('branch_number', 'status', 'user')
    ordering = ('branch_number',)
    
class AccountAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('account_number', 'account_name')
    date_hierarchy = 'create_date'
    list_filter = ('account_number', 'account_name')
    ordering = ('account_number',)
    
    
    

class PlannedAmountAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('account', 'total_amount', 'branch', 'is_acceptance_by_structure', 'is_acceptance_by_main')
    date_hierarchy = 'create_date'
    list_filter = ('account', 'branch', 'is_acceptance_by_structure', 'is_acceptance_by_main')
       
       
class StructuralDivisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('structural_division_name', 'branch')
    date_hierarchy = 'create_date'
    inlines = (AccountInline,) 
    list_filter = ('structural_division_name', 'branch')
    ordering = ('structural_division_name',)
        
    
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    date_hierarchy = 'create_date'
    inlines = (AccountInline,) 
    list_filter = ('is_active',)


        
admin.site.register(Branch, BranchAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SchedulePlan)
admin.site.register(PreviusYearFact)
admin.site.register(PerformanceIndicator)
admin.site.register(PlannedAmount, PlannedAmountAdmin)
admin.site.register(StructuralDivision, StructuralDivisionAdmin)