from django.db import models

# Create your models here.
# Create your models here.
class Weekly_Web(models.Model):
    Title = models.CharField(max_length=100)
    Released_Date = models.CharField(max_length=100)
    URL= models.CharField(max_length=100)

class position_sk_post_sum(models.Model):
    position= models.CharField(max_length=100,primary_key=True)
    dataframe =  models.CharField(max_length=1500)
    post = models.SmallIntegerField(default=0)


# class position_post_sum(models.Model):
#     position

class Web_developer_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class software_engineer_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class data_analyst_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class network_engineer_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class cloud_architect_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)



class software_tester_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class developer_programmer_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class analyst_programmer_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class ict_security_specialist_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class network_administrator_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

#class network_analyst_sk_annual(models.Model):
 #   month = models.CharField(max_length=100, default='none', primary_key=True)
  #  dataframe =  models.CharField(max_length=500, default='none')
   # post = models.SmallIntegerField(default=0)

class ict_support_engineer_sk_annual(models.Model):
    month = models.CharField(max_length=100, default='none', primary_key=True)
    dataframe =  models.CharField(max_length=1500, default='none')
    post = models.SmallIntegerField(default=0)

class jobs_pool(models.Model):
    Title = models.CharField(max_length=50, default='none')
    Released_Date =  models.CharField(max_length=40, default='none')
    URL = models.CharField(max_length=100, default='none')
    SpecificT= models.CharField(max_length=30, default='none')
    Tags= models.CharField(max_length=30, default='none')


