from django.conf.urls import include, url
from django.contrib import admin
from price_comparison_app.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'price_comparison_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', compare_algo),
]
