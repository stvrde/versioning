from django.forms.utils import flatatt
from django.http.response import HttpResponse
import software
from django.shortcuts import render,redirect
from .forms import SoftwareForm,SoftwareVersionForm,BugReportForm, RequestFeatureForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@login_required
def user_list(request):
    if request.method=="GET":
        context={
            'users':User.objects.all()
        }
        return render(request,template_name='users.html',context=context)

def register(request):

    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request,template_name='registration/register.html',context={'form':form})

def homepage(request,my_software=False,in_collaboration=False):
    bugs = []
    if my_software:
        software = Software.objects.filter(owner = request.user)
    elif in_collaboration:
        software = request.user.collabolator_in.all()
    else:
        software = Software.objects.all()

        if str(request.user) != 'AnonymousUser':
            bugs = Bug.objects.filter(version__software__owner = request.user)

    return render(request,template_name='homepage.html', context={'softwares':software,'bugs':bugs})

def software_info(request, software_id):
    return render(request,template_name='software_info.html', context={'software':Software.objects.get(pk=software_id)})

@login_required
def delete_version(request, version_id):

    softwareVersion=SoftwareVersion.objects.get(pk=version_id)
    if softwareVersion.software.owner == request.user or request.user.is_superuser:
        softwareVersion.delete()
    else:
        return no_privileges(request)
    return redirect('/')
@login_required
def edit_version(request, version_id):

    version=SoftwareVersion.objects.get(pk=version_id)

    if request.method=="GET":
        if version.software.owner == request.user or request.user.is_superuser:
            form = SoftwareVersionForm(software=version.software)
            form.initial['software']=version.software.pk
            form.initial['version']=version.version
            form.initial['description']=version.description
            if version.software.latest_version:
                form.initial['features']=list(version.software.latest_version.features.values_list('pk',flat=True))
            form.initial['requested_features']=list(version.software.requested_features.filter(accepted=False).values_list('pk',flat=True))
            form.initial['price'] = version.price
            return render(request,template_name='create_software_version.html',context={'form':form})
        else:
            return no_privileges(request)

    elif request.method=="POST":
        if version.software.owner == request.user or request.user.is_superuser:
            version.version= version.version if version_id else get_version(request,version.software)
            version.description=request.POST.get('description')
            version.modified_by= request.user.username
            version.save()
            version.features.clear()
            version.features.add(*request.POST.getlist('features'))
            return redirect('/software/info/'+str(version.software.pk))
        else:
            return no_privileges(request)

@login_required
def create_software(request,software_id=None):
    if request.method=="GET":
        form = SoftwareForm()

        if software_id:
            software= Software.objects.get(pk=software_id)
            if software.owner == request.user or request.user.is_superuser or request.user in software.team.all():
                form.initial['name']=software.name
                form.initial['price']=software.price
                form.initial['description']=software.description
                form.initial['features']=list(software.features.values_list('pk',flat=True))
                form.initial['team']=list(software.team.values_list('pk',flat=True))

            else:
                return no_privileges(request)

        return render(request,template_name='create_software.html',context={'form':form})

    elif request.method=="POST":
        newSoftware= Software.objects.get(pk=software_id) if software_id else Software()
        newSoftware.owner=request.user
        newSoftware.name=request.POST.get('name')
        newSoftware.price=request.POST.get('price')
        newSoftware.description=request.POST.get('description')
        newSoftware.created_by =newSoftware.created_by if software_id else request.user.username
        if software_id:
            newSoftware.updated_by =request.user.username

        newSoftware.save()
        if software_id:
            newSoftware.features.clear()
        newSoftware.features.add(*request.POST.getlist('features'))
        newSoftware.team.add(*request.POST.getlist('team'))

        return redirect('/')

def get_version(request,software):
    len_features = len(request.POST.getlist('requested_features'))
    len_bugs = len(request.POST.getlist('bugs'))

    if not software.latest_version:
        return '1.0.0'

    elif len_bugs>0 and len_features==0:
        version = software.latest_version
        last = version.version.split('.')[2]
        last = str(int(last)+1)
        return '.'.join(version.version.split('.')[:2])+'.'+last

    elif len_features==1:
        version = software.latest_version
        middle = version.version.split('.')[1]
        middle = str(int(middle)+1)
        return version.version.split('.')[0]+'.'+middle+'.0.'

    else:
        return str(int(software.latest_version.version.split('.')[0])+1)+'.0.0.'



@login_required
def create_software_version(request,software_id):
    software = Software.objects.get(pk=software_id)

    if request.method=="GET":
        if software.owner == request.user or request.user.is_superuser:
            form = SoftwareVersionForm(software=software)
            form.initial['software']=[software_id]
            if software.latest_version:
                form.initial['features']=list(software.latest_version.features.all().values_list('pk',flat=True))

            return render(request,template_name='create_software_version.html',context={'form':form})
        else:
            return no_privileges(request)

    elif request.method=="POST":

        if software.owner == request.user or request.user.is_superuser:
            newSoftwareVersion = SoftwareVersion()
            newSoftwareVersion.software_id = software_id
            # newSoftwareVersion.version=request.POST.get('version')
            newSoftwareVersion.version = get_version(request,software)
            newSoftwareVersion.description=request.POST.get('description')
            newSoftwareVersion.created_by = request.user.username
            newSoftwareVersion.price = request.POST.get('price')
            newSoftwareVersion.save()
            
            new_feature = request.POST.get('new_feature')
            if new_feature:
                feature = Feature.objects.create(name=new_feature)
                newSoftwareVersion.features.add(feature)

            newSoftwareVersion.features.add(*request.POST.getlist('features'))
            requested_features =request.POST.getlist('requested_features')
            newSoftwareVersion.features.add(*requested_features)

            software = Software.objects.get(pk=software_id)
            software.latest_version = newSoftwareVersion
            software.save()

            for rf_id in requested_features:
                for rf in RequestFeature.objects.filter(software=software,feature__id=rf_id):
                    rf.accepted= True
                    rf.save()

            for bug_id in request.POST.getlist('bugs'):
                bug =Bug.objects.get(pk=bug_id)
                bug.fixed=True

                bug.save()

        else:
            return no_privileges(request)

    return redirect('/')

@login_required
def delete_software(request,software_id):

    software = Software.objects.get(pk= software_id)
    if software.owner == request.user or request.user.is_superuser:
        software.delete()
        return redirect('/')

    else:
        return no_privileges(request)

@login_required
def report_bug(request,software_id):

    software=Software.objects.get(pk=software_id)

    if not software.versions.all().exists():
       return no_privileges(request,message='This software has no active versions, please create one and then report bug.')

    if request.method=="GET":
        form=BugReportForm(software=software)
        return render(request,template_name='bug_report.html',context={'form':form})

    elif request.method=="POST":
        bug = Bug()
        bug.description=request.POST.get('description')
        bug.reported_by=request.user
        bug.save()
        bug.version.add(*request.POST.getlist('version'))
    return redirect('/')

def no_privileges(request,message='You have no permissions to perform this action'):
    messages.warning(request, message)
    return redirect('/')

@login_required
def my_software(request):
    return homepage(request,my_software=True)

@login_required
def in_collaboration(request):
    return homepage(request,in_collaboration=True)

@login_required
def request_feature(request,software_id):

    if Software.objects.get(id=software_id).latest_version == None:
        messages.warning(request, 'Please create first version of software before requesting feature')
        return redirect('homepage')


    if request.method=="GET":
        form =RequestFeatureForm(software_id=software_id)
        return render(request,template_name='request_feature.html',context={'form':form})

    elif request.method=="POST":
        software= Software.objects.get(pk=software_id)
        if request.POST.get('feature'):
            new = RequestFeature()
            new.software=software
            new.user= request.user
            new.feature_id=request.POST.get('feature')
            new.save()


        new_feature = request.POST.get('new_feature')
        if new_feature:
            feature = Feature.objects.create(name=new_feature)
            new = RequestFeature()
            new.software=software
            new.user= request.user
            new.feature = feature
            new.save()
        return redirect('/')

@login_required
def bug_remove(request,id):
    Bug.objects.get(id=id).delete()
    return redirect('homepage')

@login_required
def requested_feature_remove(request,id):
    RequestFeature.objects.get(id=id).delete()
    return redirect('requested_features')

@login_required
def requested_features(request):

    return render(request,template_name='requested_features.html', context={'softwares':request.user.software.all()})
