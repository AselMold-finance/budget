from datetime import timedelta
from locale import currency
from statistics import mode
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .service import get_current_year
from django.db.models import Q, Count


class AcceptChoice(models.TextChoices):
        YES = 'yes', 'Да'
        NO = 'no', 'Нет'

class PerformanceIndicators(models.TextChoices):
        LOAN_PORTFOLIO_QUALITY = '1', 'Кредитный портфель'
        FIXED_ASSETS = '2', 'Основные средства'
        DEPOSITS = '3', 'Депозиты'
        TERM_DEPOSITS = '4', 'Срочные депозиты'
        INTEREST_EXPENSE = '5', 'Процентные расходы'
        INTEREST_EXPENSE_ON_TERM_DEPOSITS = '6', 'Процентные расходы по срочным депозитам'
        LOAN_INTEREST_INCOME = '7', 'Процентные доходы по кредитам'
        RPPU = '8', 'РППУ'
        STOCK_INTEREST_INCOME = '9', 'Процентные доходы по ЦБ'
        INTEREST_INCOME = '10', 'Процентные доходы'
        STOCK = '11', 'Ценные бумаги'
        ADMINISTRATIVE_EXPENSE = '12', 'Административные расходы'
        
        
class CurrencyType(models.TextChoices):
        RUB = 'rub', 'Рубль'
        DOLLAR = 'dollar', 'Доллар'
        EURO = 'euro', 'Евро'
        SOM = 'som', 'Сом'
        YANG = 'yang', ' Юань'
        TENGE = 'tenge', 'Тенге'
        LIRA = 'lira', 'Лира'
        WON = 'won', 'Корейский Вон'


class PerformanceIndicator(models.Model):    
    name = models.CharField(
        max_length=2,
        verbose_name='Показатель эффективности',
        choices=PerformanceIndicators.choices,
        unique=True
    )
    account_category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name='Показатель для расчёта',
    )
    
    def __str__(self,):
        return str(self.get_name_display())
    
    class Meta:
        verbose_name = 'Показатель эффективности'
        verbose_name_plural = 'Показатели эффективности'


class Branch(models.Model): 
    branch_number = models.IntegerField(
        verbose_name='Код филиала',
        unique=True
    )
    branch_name = models.CharField(
        verbose_name='Название филиала',
        blank=True,
        max_length=50,
        unique=True
    )
    branch_head_name = models.CharField(
        verbose_name='ФИО начальника филиала',
        blank=True,
        max_length=50,
        unique=True
    )
    branch_phone_number = models.CharField(
        verbose_name='Номер мобильного телефона филиала',
        max_length=20,
        unique=True,
        blank=True
    )
    branch_landline_phone_number = models.CharField(
        verbose_name='Номер стационарного телефона филиала',
        max_length=20,
        unique=True,
        blank=True
    )
    is_structual = models.BooleanField(
        verbose_name='Это структурное подразделение, а не филиал!',
        choices=AcceptChoice.choices,
        default=AcceptChoice.YES
    )
    branch_address = models.CharField(
        verbose_name='Адрес филиала',
        max_length=50,
        blank=True
    )
    branch_email = models.EmailField(
        verbose_name='Эл. почта филиала',
        max_length=50,
        blank=True
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    status = models.BooleanField(
        verbose_name='Работает',
        default=True
    )
    employee_amount = models.PositiveIntegerField(
        verbose_name='Кол-во сотрудников',
        default=0,
        blank=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='branchs'
    )
    
    def __str__(self):
        return f'{self.branch_number} | {self.user.username}'
    
    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'
    
    
class Account(models.Model):
    account_number = models.CharField(
        verbose_name='Номер счёта',
        help_text='Например 10001.00001 или 10001',
        max_length=11,
        unique=True,
        db_index=True
    )
    structure_group = models.ForeignKey(
        "StructuralDivision",
        on_delete=models.PROTECT,
        verbose_name='Название структурного подразделения'
    )
    is_strucure_planed = models.BooleanField(
        default=False,
        verbose_name='Планирование происходит структурным подразделением'
    )
    account_name = models.CharField(
        verbose_name='Название счёта',
        max_length=100,
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name='Группа счёта',
        related_name='account_category'
    )
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True
    )
    
    def __str__(self):
        return f'{self.account_number} | {self.account_name}'
    
    class Meta:
        verbose_name = 'Балансовый счёт'
        verbose_name_plural = 'Балансовые счёта'
    
    
class PreviusYearFact(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='account_fact'
    )
    amount = models.DecimalField(
        verbose_name='Факт за предыдущий год',
        max_digits=15,
        decimal_places=2
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    planed_year = models.ForeignKey(
        "SchedulePlan",
        on_delete=models.PROTECT,
    )
    
    def __str__(self):
        return str(self.account)
    
    class Meta:
        unique_together = ('account', 'planed_year')
        
    class Meta:
        verbose_name = 'Факт предыдущего года'
        verbose_name_plural = 'Факты предыдущего года'
    
    
class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название категории',
        db_index=True
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.PROTECT,
        verbose_name='Подкатегория'
    )
    is_active = models.BooleanField(
        verbose_name='Данная категория активна',
        default=True
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    ) 
    is_strucure_planed = models.BooleanField(
        default=False,
        verbose_name='Планирование происходит структурным подразделением'
    )
            
    def __str__(self) -> str:
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    
class StructuralDivision(models.Model):
    structural_division_name = models.CharField(
        max_length=50,
        verbose_name='Название структурного подразделения',
        unique=True
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        verbose_name='Структурное подразделение'
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    
    def save(self, *args, **kwargs):
        if self.branch.is_structual:
            return super().save(args, kwargs)
    
    def __str__(self):
        return f'{self.structural_division_name} | {self.user.username}'    
    
    class Meta:
        verbose_name = 'Структурное подразделение'
        verbose_name_plural = 'Структурные подразделения'
  
    
class PlannedAmount(models.Model):
    account = models.ForeignKey(
        Account,
        verbose_name='Назначение',
        on_delete=models.PROTECT,
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание или расшифровка',
        blank=True,
        default='-'
    )
    january = models.DecimalField(
        verbose_name='Сумма плана январь',
        max_digits=15,
        decimal_places=2
    )
    february = models.DecimalField(
        verbose_name='Сумма плана февраль',
        max_digits=15,
        decimal_places=2
    )
    march = models.DecimalField(
        verbose_name='Сумма плана март',
        max_digits=15,
        decimal_places=2
    )
    april = models.DecimalField(
        verbose_name='Сумма плана апрель',
        max_digits=15,
        decimal_places=2
    )
    may = models.DecimalField(
        verbose_name='Сумма плана май',
        max_digits=15,
        decimal_places=2
    )
    june = models.DecimalField(
        verbose_name='Сумма плана июнь',
        max_digits=15,
        decimal_places=2
    )
    july = models.DecimalField(
        verbose_name='Сумма плана июль',
        max_digits=15,
        decimal_places=2
    )
    august = models.DecimalField(
        verbose_name='Сумма плана август',
        max_digits=15,
        decimal_places=2
    )
    september = models.DecimalField(
        verbose_name='Сумма плана сентябрь',
        max_digits=15,
        decimal_places=2
    )
    october = models.DecimalField(
        verbose_name='Сумма плана октябрь',
        max_digits=15,
        decimal_places=2
    )
    november = models.DecimalField(
        verbose_name='Сумма плана ноябрь',
        max_digits=15,
        decimal_places=2
    )
    december = models.DecimalField(
        verbose_name='Сумма плана декабрь',
        max_digits=15,
        decimal_places=2
    )
    branch = models.ForeignKey(
        Branch,
        verbose_name='Филиал',
        on_delete=models.PROTECT
    )
    is_add = models.BooleanField(
        verbose_name='Добавлен',
        default=False
    )
    is_acceptance_by_structure = models.BooleanField(
        verbose_name='Акцептован структурным подразделением',
        default=False
    )
    is_acceptance_by_main = models.BooleanField(
        verbose_name='Акцептован отделом планирования',
        default=False
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    planed_year = models.ForeignKey(
        "SchedulePlan",
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.PROTECT,
        verbose_name='Валюта бюджетирования'
    )
    
    def total_amount(self,):
        all_month = (
            self.january,
            self.february,
            self.march,
            self.april,
            self.may,
            self.june,
            self.july,
            self.august,
            self.september,
            self.october,
            self.november,
            self.december
        )
        return sum(all_month)
    
    def __str__(self):
        return f'{self.account} | {self.total_amount()} | {self.branch}'
    
    
    class Meta:
        unique_together = ('account', 'planed_year',)
        verbose_name = 'Плановая сумма'
        verbose_name_plural = 'Плановые суммы'

    
class SchedulePlan(models.Model):
    
    year = models.PositiveIntegerField(
        default=get_current_year,
        verbose_name='Год бюджетирования',
        validators=[
                MinValueValidator(1900), 
                MaxValueValidator(timezone.now().year)],
        help_text="Используйте указанный формат: <YYYY>",
        unique=True
                               )
    edit_start_date = models.DateTimeField(
        verbose_name='Дата начала редактирования бюджета'
    )
    edit_end_date = models.DateTimeField(
        verbose_name='Дата конца редактирования бюджета'
    )
    accept_start_date = models.DateTimeField(
        verbose_name='Дата начала акцептирования бюджета'
    )
    accept_end_date = models.DateTimeField(
        verbose_name='Дата конца акцептирования бюджета'
    )
    is_edit = models.BooleanField(
        verbose_name='Редактирование',
        default=True
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    
    def __str__(self):
        return f'{self.year}'
    
    class Meta:
        verbose_name = 'График бюджетирования'
        verbose_name_plural = 'Графики бюджетирования'


class Currency(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Наименование Валюты',
        choices=CurrencyType.choices,
        default=CurrencyType.SOM,
        unique=True
    )
    currency = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Курс валюты',
        validators=[
            MinValueValidator(0)
            ]
    )
    currency_planed_year = models.ForeignKey(
        SchedulePlan,
        on_delete=models.PROTECT,
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    