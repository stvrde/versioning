from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class AuditFields(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=50,null=True,blank=True)
    modified_at = models.DateTimeField(default=timezone.now)
    modified_by = models.CharField(max_length=50,null=True,blank=True)

    class Meta:
        abstract = True

class Software(AuditFields):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User,related_name='software',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description =models.CharField(max_length=1024)
    features= models.ManyToManyField('Feature',related_name='software')

    latest_version =  models.ForeignKey('SoftwareVersion',null=True,blank=True,default=None,on_delete=models.SET_NULL,related_name='latest_version')

    team = models.ManyToManyField(User,related_name='collabolator_in')

    def __str__(self):
        return self.name

    def feature_list(self):
        return self.features.values_list("name", flat=True)

    def users_in_team(self):
        return ','.join(self.team.values_list('username',flat=True))

class Feature(AuditFields):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

        
class SoftwareVersion(AuditFields):
    software = models.ForeignKey('Software',on_delete=models.CASCADE,related_name='versions')
    version = models.CharField(max_length=10)
    features = models.ManyToManyField(Feature)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)

    description = models.CharField(max_length=1024)
    def __str__(self):
        return str(self.version)

    def feature_list(self):
        return self.features.values_list("name", flat=True)

class Bug(AuditFields):
    version = models.ManyToManyField(SoftwareVersion,related_name='bugs')
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bugs')
    description = models.CharField(max_length=1024)
    fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class RequestFeature(AuditFields):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='requested_features')
    software = models.ForeignKey('Software',on_delete=models.CASCADE,related_name='requested_features')
    feature = models.ForeignKey('Feature',on_delete=models.CASCADE,related_name='requested_features')
    accepted = models.BooleanField(default=False)
  
    def __str__(self):
        return str(self.feature)