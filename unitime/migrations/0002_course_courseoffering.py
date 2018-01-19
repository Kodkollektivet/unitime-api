# Generated by Django 2.0.1 on 2018-01-17 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unitime', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=254)),
                ('speed', models.CharField(max_length=20)),
                ('points', models.CharField(max_length=20)),
                ('syllabus', models.CharField(max_length=254)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseOffering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('offering_id', models.CharField(max_length=254)),
                ('registration_id', models.CharField(max_length=254)),
                ('year', models.CharField(max_length=254)),
                ('semester', models.CharField(max_length=254)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unitime.Course')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
