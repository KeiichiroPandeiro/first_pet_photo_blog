# Generated by Django 2.1.2 on 2018-11-11 15:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_auto_20181111_0330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('sex', models.IntegerField(choices=[(0, 'オス'), (1, 'メス'), (2, '秘密')], default=0, verbose_name='性別')),
                ('together_with', models.IntegerField(default=1985, validators=[django.core.validators.MinValueValidator(1985)])),
                ('pet_type', models.IntegerField(choices=[(0, '犬'), (1, '猫'), (2, 'その他')], default=0, verbose_name='ペットの種類')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='pet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Pet'),
        ),
    ]
