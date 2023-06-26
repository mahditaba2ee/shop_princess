from django.core.management import BaseCommand
from Accounts.models import OtpCodeModel
from datetime import datetime ,timedelta
import pytz
from celery import shared_task

@shared_task
def remove_expired_otp():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    OtpCodeModel.objects.filter(created__lt=expired_time).delete()
        
    