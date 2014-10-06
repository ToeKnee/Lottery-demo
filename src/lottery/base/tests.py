from django.contrib.auth.models import AnonymousUser
from django.test import (
    TestCase,
    RequestFactory,
)


from .factories import UserFactory
from .test_utils import strip_spaces_from_html
from .views import home
from lottery.lotto.factories import ActiveLotteryFactory


class HomeView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_anonymous__no_lotteries(self):
        request = self.factory.get('')
        request.user = AnonymousUser()

        response = home(request)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertIn("No lotteries active", content)

    def test_anonymous__with_lottery(self):
        lottery = ActiveLotteryFactory()
        request = self.factory.get('')
        request.user = AnonymousUser()

        response = home(request)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertIn(lottery.title, content)
        self.assertIn(lottery.get_absolute_url(), content)

    def test_no_lotteries(self):
        user = UserFactory()
        request = self.factory.get('')
        request.user = user

        response = home(request)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertIn("No lotteries active", content)

    def test_with_lottery__not_entered(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()
        request = self.factory.get('')
        request.user = user

        response = home(request)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertIn(lottery.title, content)
        self.assertIn(lottery.get_absolute_url(), content)

    def test_with_lottery_entered(self):
        lottery = ActiveLotteryFactory()
        user = UserFactory()
        lottery.entrants.add(user)

        request = self.factory.get('')
        request.user = user

        response = home(request)
        self.assertEqual(200, response.status_code)
        content = strip_spaces_from_html(response.content)
        self.assertIn(lottery.title, content)
        self.assertNotIn(lottery.get_absolute_url(), content)
