from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Data(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    create_time = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    head = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'data'


# 服务器IP
MEDIA_ADDR = 'http://localhost:8000/media/'


class user_info_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portrait = models.ImageField(upload_to='portrait', blank=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    # username =

    class Meta:
        managed = True
        db_table = 'user_info_data'

    def get_portrait_url(self):
        """返回头像的url"""
        return MEDIA_ADDR + str(self.portrait)

    def get_phone(self):
        return str(self.phone)


class follow(models.Model):
    username = models.CharField(max_length=10, blank=True)
    follow_city = models.CharField(max_length=10, blank=True)
    follow_category = models.CharField(max_length=10, blank=True)
    last_time = models.DateField(blank=True, null=True)


class GovUrl(models.Model):
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gov_url'


class PolicyUrl(models.Model):
    policy_url = models.URLField(blank=True, null=True)
    policy_title = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    create_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'policy_url'
