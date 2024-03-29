# Generated by Django 3.0.5 on 2020-04-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coronadaily',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('dailyconfirmed', models.IntegerField()),
                ('dailydeceased', models.IntegerField()),
                ('dailyrecovered', models.IntegerField()),
                ('totalconfirmed', models.IntegerField()),
                ('totaldeceased', models.IntegerField()),
                ('totalrecovered', models.IntegerField()),
            ],
            options={
                'db_table': 'coronadaily',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Coronastatedaily',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('loc', models.CharField(max_length=50)),
                ('confirmedcasesforeign', models.IntegerField(db_column='confirmedCasesForeign')),
                ('confirmedcasesindian', models.IntegerField(db_column='confirmedCasesIndian')),
                ('deaths', models.IntegerField()),
                ('discharged', models.IntegerField()),
                ('totalconfirmed', models.IntegerField()),
            ],
            options={
                'db_table': 'coronastatedaily',
                'managed': False,
            },
        ),
    ]
