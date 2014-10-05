import mock
import unittest

from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import (
    ActiveLotteryFactory,
    InactiveLotteryFactory,
    FutureLotteryFactory,
    PastLotteryFactory,
)
from .models import Lottery
from lottery.base.factories import UserFactory


class LotteryActiveManagerTest(TestCase):
    def test_active_started(self):
        lottery = ActiveLotteryFactory()
        self.assertIn(lottery, Lottery.objects.active())

    def test_active_not_started(self):
        lottery = FutureLotteryFactory()
        self.assertNotIn(lottery, Lottery.objects.active())

    def test_active_finished(self):
        lottery = PastLotteryFactory()
        self.assertNotIn(lottery, Lottery.objects.active())

    def test_inactive_started(self):
        lottery = InactiveLotteryFactory()
        self.assertNotIn(lottery, Lottery.objects.active())


# As we aren't using the database, we can use unittest.TestCase and
# avoid setting up transactions
class LotteryTest(unittest.TestCase):
    def test_unicode(self):
        lottery = ActiveLotteryFactory.build()  # Don't store in the database
        self.assertEqual(unicode(lottery), lottery.title)

    def test_get_absolute_url(self):
        lottery = ActiveLotteryFactory.build()  # Don't store in the database
        self.assertEqual(
            reverse("lottery_detail", kwargs={"slug": lottery.slug}),
            lottery.get_absolute_url()
        )


class LotteryUserTest(TestCase):
    def setUp(self):
        self.lottery = ActiveLotteryFactory()
        self.user = UserFactory()

    def test_entered(self):
        self.lottery.entrants.add(self.user)
        self.assertTrue(self.lottery.has_entered(self.user.pk))

    def test_not_entered(self):
        self.assertFalse(self.lottery.has_entered(self.user.pk))

    def test_won(self):
        self.lottery.winners.add(self.user)
        self.assertTrue(self.lottery.has_won(self.user.pk))

    def test_now_won(self):
        self.assertFalse(self.lottery.has_won(self.user.pk))

    def test_check_win_condition__win(self):
        with mock.patch('random.getrandbits', return_value=1):
            self.assertTrue(self.lottery.check_win_condition(self.user))

    def test_check_win_condition__lose(self):
        with mock.patch('random.getrandbits', return_value=0):
            self.assertFalse(self.lottery.check_win_condition(self.user))

    def test_enter__win(self):
        with mock.patch('random.getrandbits', return_value=1):
            self.assertTrue(self.lottery.enter(self.user))

    def test_enter__lose(self):
        with mock.patch('random.getrandbits', return_value=0):
            self.assertFalse(self.lottery.enter(self.user))

    def test_enter__already_entered_and_won(self):
        self.lottery.entrants.add(self.user)
        self.lottery.winners.add(self.user)
        self.assertTrue(self.lottery.enter(self.user))

    def test_enter__already_entered_and_lost(self):
        self.lottery.entrants.add(self.user)
        self.assertFalse(self.lottery.enter(self.user))
