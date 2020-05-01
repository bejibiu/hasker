from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=user_directory_path, null=True)
    date_of_create = models.DateTimeField(auto_now_add=True)

    def get_url_avatar(self):
        if self.avatar.name:
            return f"{settings.MEDIA_URL}{self.avatar.name}"
        return f"{settings.STATIC_URL}img/default_user_icon.jpg"


@receiver(post_save, sender=User)
def create_account_for_new_user(sender, instance, created, **kwargs):
    if created:
        account = Account(user=instance)
        account.save()
