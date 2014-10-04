from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Lottery(models.Model):
    slug = models.SlugField(max_length=255, unique=True, help_text=_("Automatically pre-populated from title"))
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    entrants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lottery_entered")
    winners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lottery_won")

    class Meta:
        verbose_name_plural = _("Lotteries")

    def __unicode__(self):
        return self.title
