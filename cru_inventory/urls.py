"""cru_inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^helm/', admin.site.urls, name="helm"),
    url(r'^$', RedirectView.as_view(url=reverse_lazy("inv:items"), permanent=False)),
    url(r'^login/', auth_views.login, {'template_name': 'admin/login.html'}, name="login"),
    url(r'^logout/', auth_views.logout, {'next_page': reverse_lazy('login')}, name="logout"),
    url(r'^inventory/', include('inventory.urls', namespace='inv')),
]
