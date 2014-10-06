from django.conf.urls import patterns, url

urlpatterns = patterns(
    'lottery.lotto.views',

    url(r'^$', 'list_view', name='lotteries_list'),
    url(r'^(?P<slug>[a-z0-9_-]+)/$', 'detail', name='lottery_detail'),
)
