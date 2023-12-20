from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import GeneralInfoModel
from django.dispatch import receiver

@receiver(post_save, sender=User)
def Create_GeneralInfo(sender, **kwargs):
    if kwargs['created']:
        GeneralInfoModel.objects.create(user=kwargs['instance'])