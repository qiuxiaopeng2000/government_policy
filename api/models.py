from django.db import models


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


class GovUrl(models.Model):
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    belong_to = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gov_url'


class PolicyUrl(models.Model):
    policy_url = models.URLField(blank=True, null=True)
    policy_title = models.TextField(blank=True, null=True)
    belong_to = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    create_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'policy_url'