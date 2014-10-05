from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    url(r'^$', 'lottery.base.views.home', name='home'),
    url(r'^lottery/', include('lottery.lotto.urls')),

    url(r'^admin/', include(admin.site.urls)),

)

# Static files
urlpatterns += staticfiles_urlpatterns()
