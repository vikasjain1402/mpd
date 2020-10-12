from django.db import models


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
