# Generated by Django 3.0 on 2019-12-29 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_custm_user_createtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='custm_user',
            name='sxj',
            field=models.CharField(default='dsds', max_length=50, verbose_name='sss'),
            preserve_default=False,
        ),
    ]
