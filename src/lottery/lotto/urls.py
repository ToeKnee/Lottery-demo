from django.conf.urls import patterns, url

urlpatterns = patterns(
    'lottery.lotto.views',

    url(r'^$', 'list', name='lotteries_list'),
)
