"""Versioning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('', views.homepage,name='homepage'),

    path('software/info/<int:software_id>', views.software_info, name='software_info'),
    path('software/version/delete/<int:version_id>', views.delete_version, name='delete_version'),
    path('software/version/edit/<int:version_id>', views.edit_version, name='edit_version'),

    path('software/bug/add/<int:software_id>', views.report_bug, name='report_bug'),


    path('software/create', views.create_software,name='create_software'),
    path('software/delete/<int:software_id>', views.delete_software,name='delete_software'),
    path('software/edit/<int:software_id>', views.create_software,name='edit_software'),
    path('software/createVersion/<int:software_id>', views.create_software_version,name='create_software_version'),
    path('auth/', include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
    path('users/',views.user_list,name='user_list'),
    path('my_software/',views.my_software,name='my_software'),
    path('in_collaboration/',views.in_collaboration,name='in_collaboration'),
    path('request_feature/<int:software_id>',views.request_feature,name='request_feature'),
    path('requested_features',views.requested_features,name='requested_features'),

    path('bug/remove/<int:id>',views.bug_remove,name='bug_remove'),
    path('requested_feature/remove/<int:id>',views.requested_feature_remove,name='requested_feature_remove'),
]
