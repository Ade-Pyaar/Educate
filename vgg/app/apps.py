from django.apps import AppConfig
from django.db.models.signals import post_migrate



# def create_required_objects(sender, **kwargs):
#     from .models import Subscription
#     import json
#     all_subs = Subscription.objects.all()
#     if len(all_subs) < 1:
#         latest_sub = Subscription()
#         latest_sub.subscription = json.dumps({})
#         latest_sub.save()


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # def ready(self):
    #     post_migrate.connect(create_required_objects, sender=self)
