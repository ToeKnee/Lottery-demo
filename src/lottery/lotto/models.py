import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class LotteryManager(models.Manager):
    def active(self):
        now = timezone.now()
        return self.filter(active=True, start_date__lte=now, end_date__gte=now)


def default_end_date():
    return timezone.now() + datetime.timedelta(days=14)


class Lottery(models.Model):
    slug = models.SlugField(max_length=255, unique=True, help_text=_("Automatically pre-populated from title"))
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=default_end_date)

    entrants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lottery_entered")
    winners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lottery_won")

    objects = LotteryManager()

    class Meta:
        verbose_name_plural = _("Lotteries")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("lottery_detail", kwargs={"slug": self.slug})

    def has_entered(self, user_id):
        return bool(self.entrants.filter(pk=user_id).count())

    def has_won(self, user_id):
        return bool(self.winners.filter(id=user_id).count())
