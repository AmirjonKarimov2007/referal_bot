# Generated by Django 5.0 on 2024-11-22 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Username'),
        ),
    ]