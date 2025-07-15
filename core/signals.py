from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .mystral import is_bad_review

@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    # Created - это флаг, который показывает, что запись была создана
    # if created:
    return 