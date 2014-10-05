import mock
import unittest

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import (
    TestCase,
    RequestFactory,
)

from .factories import (
    ActiveLotteryFactory,
    InactiveLotteryFactory,
    FutureLotteryFactory,
    PastLotteryFactory,
)
from .models import Lottery
from .views import detail
from lottery.base.factories import UserFactory
from lottery.base.test_utils import strip_spaces_from_html


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

    def test_entrants_count(self):
        self.assertEqual(0, self.lottery.entrants_count())
        self.lottery.entrants.add(self.user)
        self.assertEqual(1, self.lottery.entrants_count())

    def test_winners_count(self):
        self.assertEqual(0, self.lottery.winners_count())
        self.lottery.winners.add(self.user)
        self.assertEqual(1, self.lottery.winners_count())

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


class DetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_inactive_lottery_should_404(self):
        lottery = InactiveLotteryFactory()

        request = self.factory.get('')
        request.user = AnonymousUser()

        with self.assertRaises(Http404):
            detail(request, lottery.slug)

    def test_anonymous(self):
        lottery = ActiveLotteryFactory()

        request = self.factory.get('')
        request.user = AnonymousUser()

        response = detail(request, lottery.slug)
        self.assertEqual(200, response.status_code)
        self.assertIn("You must log-in to play the lottery.", response.content)

    def test_get_not_entered(self):
        lottery = ActiveLotteryFactory()

        request = self.factory.get('')
        request.user = UserFactory()

        response = detail(request, lottery.slug)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertIn("Enter the lottery!", content)
        self.assertIn("<form", content)
        self.assertIn("type=\"submit\"", content)

    def test_get_won(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()
        lottery.entrants.add(user)
        lottery.winners.add(user)

        request = self.factory.get('')
        request.user = user

        response = detail(request, lottery.slug)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertNotIn("Enter the lottery!", content)
        self.assertNotIn("<form", content)
        self.assertNotIn("type=\"submit\"", content)
        self.assertIn("You have entered this lottery and have won", content)

    def test_get_lost(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()
        lottery.entrants.add(user)

        request = self.factory.get('')
        request.user = user

        response = detail(request, lottery.slug)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertNotIn("Enter the lottery!", content)
        self.assertNotIn("<form", content)
        self.assertNotIn("type=\"submit\"", content)
        self.assertIn("You have entered this lottery and have not won", content)

    def test_post_not_entered__winning(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()

        request = self.factory.post('')
        request.user = user

        with mock.patch('random.getrandbits', return_value=1):
            response = detail(request, lottery.slug)
            self.assertEqual(302, response.status_code)
            location = response._headers["location"][1]
            self.assertEqual(location, lottery.get_absolute_url())
            self.assertTrue(lottery.has_entered(user.id))
            self.assertTrue(lottery.has_won(user.id))

    def test_post_not_entered__losing(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()

        request = self.factory.post('')
        request.user = user

        with mock.patch('random.getrandbits', return_value=0):
            response = detail(request, lottery.slug)
            self.assertEqual(302, response.status_code)
            location = response._headers["location"][1]
            self.assertEqual(location, lottery.get_absolute_url())
            self.assertTrue(lottery.has_entered(user.id))
            self.assertFalse(lottery.has_won(user.id))

    def test_post_already_won(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()
        lottery.entrants.add(user)
        lottery.winners.add(user)

        request = self.factory.post('')
        request.user = user

        # This will return the "lost" if they have not already won.
        # But as they have, they will still have won
        with mock.patch('random.getrandbits', return_value=0):
            response = detail(request, lottery.slug)
            self.assertEqual(302, response.status_code)
            location = response._headers["location"][1]
            self.assertEqual(location, lottery.get_absolute_url())
            self.assertTrue(lottery.has_entered(user.id))
            self.assertTrue(lottery.has_won(user.id))

    def test_post_already_lost(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()
        lottery.entrants.add(user)

        request = self.factory.post('')
        request.user = user

        # This will return the "won" if they have not already lost.
        # But as they have, they will still have lost
        with mock.patch('random.getrandbits', return_value=1):
            response = detail(request, lottery.slug)
            self.assertEqual(302, response.status_code)
            location = response._headers["location"][1]
            self.assertEqual(location, lottery.get_absolute_url())
            self.assertTrue(lottery.has_entered(user.id))
            self.assertFalse(lottery.has_won(user.id))
