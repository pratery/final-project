# Generated by Django 4.0.4 on 2022-04-20 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='foo',
            field=models.CharField(default='banana', max_length=100),
            preserve_default=False,
        ),
    ]
