from django.shortcuts import render
from lottery.lotto.models import Lottery


def home(request):
    if request.user.is_anonymous():
        lotteries_entered = []
        lotteries_open = Lottery.objects.active()
    else:
        lotteries_entered = Lottery.objects.active().filter(entrants=request.user)
        lotteries_open = Lottery.objects.active().exclude(entrants=request.user)
    context = {
        "lotteries_entered": lotteries_entered,
        "lotteries_open": lotteries_open,
    }
    return render(request, "home.html", context)
