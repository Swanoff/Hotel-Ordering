# Generated by Django 2.0.2 on 2019-03-26 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20190322_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='addon_res',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='addons',
            name='cost',
            field=models.PositiveIntegerField(default=1000, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addon_res',
            name='a_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.addons'),
        ),
        migrations.AddField(
            model_name='addon_res',
            name='r_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.reservations'),
        ),
    ]
