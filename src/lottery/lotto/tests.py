import unittest
from django.test import TestCase

from .factories import (
    ActiveLotteryFactory,
    InactiveLotteryFactory,
    FutureLotteryFactory,
    PastLotteryFactory,
)
from .models import Lottery


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
