import datetime
import random

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

    entrants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lotteries_entered", null=True, blank=True, editable=False)
    winners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lotteries_won", null=True, blank=True)

    objects = LotteryManager()

    class Meta:
        verbose_name_plural = _("Lotteries")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("lottery_detail", kwargs={"slug": self.slug})

    def entrants_count(self):
        return self.entrants.count()

    def winners_count(self):
        return self.winners.count()

    def has_entered(self, user_id):
        return bool(self.entrants.filter(pk=user_id).count())

    def has_won(self, user_id):
        return bool(self.winners.filter(id=user_id).count())

    def check_win_condition(self, user):
        """ Flip a coin to see if they have won
        Pretty sure this lottery will go broke soon...
        """
        # About twice as fast as the more obvious random.choice([True, False])
        return bool(random.getrandbits(1))

    def enter(self, user):
        """ Enter the lottery, and return if the user has won or not.
        If the user has already one, return if they have won already.
        """

        if not self.has_entered(user.id):
            self.entrants.add(user)
            has_won = self.check_win_condition(user)
            if has_won:
                self.winners.add(user)
        else:
            has_won = self.has_won(user.id)
        return has_won
