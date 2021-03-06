# Generated by Django 3.2.3 on 2021-07-14 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postsite', '0005_alter_user_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='ヘッダー画像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Eメールアドレス'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, verbose_name='ユーザー名'),
        ),
    ]
