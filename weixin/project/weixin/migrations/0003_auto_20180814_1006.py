# Generated by Django 2.0.7 on 2018-08-14 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0002_auto_20180813_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='invitenumber',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='邀请码'),
        ),
        migrations.AlterField(
            model_name='member',
            name='Mcardnum2',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='member',
            name='Mcardnum3',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='member',
            name='Mcardnum4',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='收货地址'),
        ),
    ]