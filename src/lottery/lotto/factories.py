import datetime
import factory

from django.template.defaultfilters import slugify
from django.utils import timezone

from .models import Lottery


class InactiveLotteryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Lottery

    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    title = factory.Sequence(lambda n: 'Lottery #{n}'.format(n=n))
    description = "A description of the lottery"


class ActiveLotteryFactory(InactiveLotteryFactory):
    active = True


class FutureLotteryFactory(ActiveLotteryFactory):
    start_date = factory.LazyAttribute(lambda o: timezone.now() + datetime.timedelta(days=1))


class PastLotteryFactory(ActiveLotteryFactory):
    start_date = factory.LazyAttribute(lambda o: timezone.now() - datetime.timedelta(days=14))
    end_date = factory.LazyAttribute(lambda o: timezone.now() - datetime.timedelta(days=1))
