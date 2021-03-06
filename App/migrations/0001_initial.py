# Generated by Django 3.0 on 2019-12-08 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
                ('trackid', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='MainNav',
            fields=[
                ('main_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='App.Main')),
            ],
            options={
                'db_table': 'axf_nav',
            },
            bases=('App.main',),
        ),
        migrations.CreateModel(
            name='MainWheel',
            fields=[
                ('main_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='App.Main')),
            ],
            options={
                'db_table': 'axf_wheel',
            },
            bases=('App.main',),
        ),
    ]
