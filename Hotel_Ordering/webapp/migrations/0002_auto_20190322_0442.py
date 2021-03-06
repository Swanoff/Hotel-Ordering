# Generated by Django 2.0.2 on 2019-03-22 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='addons',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('addon', models.CharField(max_length=20)),
                ('pre_book', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='reservations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='room_type',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=10)),
                ('cost', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('image', models.ImageField(upload_to='webapp/room_pics')),
                ('room_no', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=20000)),
                ('occupied', models.BooleanField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.room_type')),
            ],
        ),
        migrations.AddField(
            model_name='reservations',
            name='r_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.rooms'),
        ),
        migrations.AddField(
            model_name='reservations',
            name='u_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addons',
            name='f_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.room_type'),
        ),
    ]
