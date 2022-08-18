from django.utils import timezone
from django.db.models import F

def get_current_year():
    return timezone.now().year

def get_calc_month(month=12):
    months = (F('january'), F('february'), F('march'), F('april'), F('may'), F('june'), F('july'), F('august'), F('september'), F('october'), F('november'), F('december'))
    return months[:month]
