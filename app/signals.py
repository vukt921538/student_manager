from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=HocKi)
def create_history(sender, instance, *args, **kwargs):
    print('SOMEONE_OK_NOW')

