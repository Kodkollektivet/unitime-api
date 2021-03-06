# Generated by Django 2.0.1 on 2018-01-18 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitime', '0011_auto_20180118_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=254, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set(),
        ),
    ]
