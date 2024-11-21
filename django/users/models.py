from django.db import models

class User(models.Model):
    name = models.CharField(verbose_name='Fullname', max_length=100)
    username = models.CharField(verbose_name='Username', max_length=100, null=True,blank=True)
    user_id = models.BigIntegerField(verbose_name='Telegram_id', unique=True, default=1)
    balance = models.BigIntegerField(verbose_name='Balance',default=0,null=True,blank=True)
    number = models.BigIntegerField(verbose_name="Telefon raqami",null=True,blank=True)
    ref_father = models.BigIntegerField(verbose_name='ref_father',null=True,blank=True)
    register = models.BooleanField(default=False)
    def __str__(self):
        return self.name

