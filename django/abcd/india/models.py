
from django.db import models


class Coronadaily(models.Model):
    date = models.DateField(primary_key=True)
    dailyconfirmed = models.IntegerField()
    dailydeceased = models.IntegerField()
    dailyrecovered = models.IntegerField()
    totalconfirmed = models.IntegerField()
    totaldeceased = models.IntegerField()
    totalrecovered = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coronadaily'



class Coronastatedaily(models.Model):
    date = models.DateField(primary_key=True)
    loc = models.CharField(max_length=50)
    population = models.IntegerField()  # Field name made lowercase.
    tested = models.IntegerField()  # Field name made lowercase.
    deaths = models.IntegerField()
    discharged = models.IntegerField()
    totalconfirmed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coronastatedaily'
        unique_together = (('date', 'loc'),)


'''
class Coronastatedaily(models.Model):
    date = models.DateField(primary_key=True)
    loc = models.CharField(max_length=50)
    confirmedcasesforeign = models.IntegerField(db_column='confirmedCasesForeign')  # Field name made lowercase.
    confirmedcasesindian = models.IntegerField(db_column='confirmedCasesIndian')  # Field name made lowercase.
    deaths = models.IntegerField()
    discharged = models.IntegerField()
    totalconfirmed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coronastatedaily'
        unique_together = (('date', 'loc'),)

'''
class Districtdaily(models.Model):
    state = models.CharField(primary_key=True, max_length=50)
    district = models.CharField(max_length=30)
    date = models.DateField()
    active = models.IntegerField()
    confirmed = models.IntegerField()
    deceased = models.IntegerField()
    recovered = models.IntegerField()
    population = models.IntegerField()
    tested = models.IntegerField()


    class Meta:
        managed = False
        db_table = 'districtdaily'
        unique_together = (('state', 'district', 'date'),)

class Coronaworld1(models.Model):
    country_name = models.CharField(primary_key=True, max_length=50)
    cases = models.IntegerField()
    deaths = models.IntegerField()
    region = models.CharField(max_length=50)
    total_recovered = models.IntegerField()
    new_deaths = models.IntegerField()
    new_cases = models.IntegerField()
    serious_critical = models.IntegerField()
    active_cases = models.IntegerField()
    total_cases_per_1m_population = models.IntegerField()
    date = models.DateTimeField()
    deaths_per_1m_population = models.IntegerField(blank=True, null=True)
    tests_per_1m_population = models.IntegerField(blank=True, null=True)
    total_tests = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coronaworld1'
        unique_together = (('country_name', 'date'),)

class picture(models.Model):
    location=models.ImageField(upload_to='pics')
    disc=models.CharField(max_length=15)
