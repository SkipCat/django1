# Generated by Django 2.1.2 on 2018-11-18 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Markdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('alias', models.CharField(blank=True, max_length=200, unique=True)),
            ],
        ),
    ]