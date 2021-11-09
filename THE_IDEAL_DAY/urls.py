"""THE_IDEAL_DAY URL Configuration

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
from django.urls import include,path
from django.conf.urls import url
from idealday.api import analytics, view_plan, add_intrvl, today
urlpatterns = [
    path('idealday/', include('idealday.urls')),
    path('admin/', admin.site.urls),
    url('view_plan/',view_plan.as_view(),name='view'),
    url('add_intrvl/',add_intrvl.as_view(),name='add'),
    url('today/',today.as_view(),name='today'),
    url('analytics',analytics.as_view(),name='analytics')
]
