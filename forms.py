from django import forms
from django.forms.fields import CharField
from django.http import request
from software import models


class SoftwareForm(forms.Form):

    name =forms.CharField(
        label       = 'Software name',
        max_length  = 255, 
        widget      = forms.TextInput(attrs={'class':'form-control','placeholder':'Please input software name'})
        )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget = forms.NumberInput(attrs={'class':'form-control'})
    )

    choices = models.Feature.objects.all()
    features = forms.ModelMultipleChoiceField(
        label    = 'Features',
        required = True,
        queryset  = choices,
        widget   = forms.SelectMultiple(attrs={'class':'form-control','size':len(choices) if len(choices)<=8 else 8})
    ) 

    description= forms.CharField(
        label       = 'Software description',
        max_length  = 1024, 
        widget      = forms.Textarea(attrs={'class':'form-control','placeholder':'Describe your software','rows':"5"})
        )

    team = forms.ModelMultipleChoiceField(
        label    = 'Select collaborators',
        required = True,
        queryset  = models.User.objects.all(),
        widget   = forms.SelectMultiple(attrs={'class':'form-control','size':len(choices) if len(choices)<=8 else 8})
    ) 

class SoftwareVersionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        software = kwargs.pop('software')
        super().__init__(*args, **kwargs)
        if software:
            if software.latest_version:
                self.fields['features'].queryset = software.latest_version.features.all().union(software.features.all())
            else:
                self.fields['features'].queryset = software.features.all()

            requested_features=software.requested_features.filter(accepted=False)
            features = [rf.feature.pk for rf in requested_features]
            qs =models.Feature.objects.filter(pk__in=features)
            if qs.exists():
                self.fields['requested_features'].queryset = qs
            else:
                self.fields['requested_features']=None
            if software.latest_version:
                self.fields['bugs'].queryset = models.Bug.objects.filter(fixed=False,version__software=software)
            else:
                self.fields['bugs']=None



    choices = models.Software.objects.all()
    software =forms.ModelMultipleChoiceField(
        label    = 'Software',
        required = True,
        queryset  = choices,
        widget   = forms.SelectMultiple(attrs={'class':'form-control','size':len(choices) if len(choices)<=8 else 8})
        ) 
    
    # version = forms.CharField(
    #     label       = 'Version number',
    #     max_length  = 64, 
    #     widget      = forms.TextInput(attrs={'class':'form-control','placeholder':'Please input version number'})
    # )

    features =forms.ModelMultipleChoiceField(
        label    = 'Features',
        required = False,
        queryset  = None,
        widget   = forms.SelectMultiple(attrs={'class':'form-control'})
        ) 
    new_feature = forms.CharField(
        label       = 'Add new feature',
        max_length  = 64, 
        required=False,
        widget      = forms.TextInput(attrs={'class':'form-control','placeholder':'Please input feature name'})
        )
    bugs =forms.ModelMultipleChoiceField(
        label    = 'Bugs fixed',
        required = False,
        queryset  = None,
        widget   = forms.SelectMultiple(attrs={'class':'form-control'})
        )
    
    description = forms.CharField(
        label       = 'Version description',
        max_length  = 1024, 
        widget      = forms.Textarea(attrs={'class':'form-control','placeholder':'Describe your version','rows':"5"})
        )

    requested_features = forms.ModelMultipleChoiceField(
        label    = 'Add requested features',
        required = False,
        queryset  = None,
        widget   = forms.SelectMultiple(attrs={'class':'form-control'})
        ) 
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget = forms.NumberInput(attrs={'class':'form-control'})
    )

class BugReportForm(forms.Form):

    def __init__(self, *args, **kwargs):
        software = kwargs.pop('software')
        super().__init__(*args, **kwargs)
        if software:
            self.fields['version'].queryset = software.versions.all()

    version =forms.ModelMultipleChoiceField(
        label    = 'Select version for which you want to report a Bug',
        required = True,
        queryset  = None,
        widget   = forms.SelectMultiple(attrs={'class':'form-control','size':5})
        ) 

    description = forms.CharField(
        label       = 'Bug description',
        max_length  = 1024, 
        widget      = forms.Textarea(attrs={'class':'form-control','placeholder':'Describe bug you have found...','rows':"5"})
        )

class RequestFeatureForm(forms.Form):

    def __init__(self, *args, **kwargs):
        software = kwargs.pop('software_id')
        super().__init__(*args, **kwargs)
        if software:
            self.fields['feature'].queryset = models.Feature.objects.all().exclude(pk__in = models.Software.objects.get(pk=software).latest_version.features.values_list('pk'))
    feature =forms.ModelMultipleChoiceField(
        label    = 'Feature',
        required = False,
        queryset  = None,
        widget   = forms.SelectMultiple(attrs={'class':'form-control'})
        )
    new_feature = forms.CharField(
        label       = 'Add new feature',
        max_length  = 64, 
        required=False,
        widget      = forms.TextInput(attrs={'class':'form-control','placeholder':'Please input feature name'})
        )