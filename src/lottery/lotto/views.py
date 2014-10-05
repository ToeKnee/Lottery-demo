from django.shortcuts import (
    get_object_or_404,
    render,
)

from .models import Lottery


def list(request):
    lotteries = Lottery.objects.active().exclude(entrants=request.user)
    context = {
        "lotteries": lotteries,
    }
    return render(request, "lotto/list.html", context)


def detail(request, slug):
    lottery = get_object_or_404(Lottery.objects.active(), slug=slug)
    if request.user.is_anonymous():
        entered = False
        won = False
    else:
        entered = lottery.has_entered(request.user.id)
        if entered:
            won = lottery.has_won(request.user.id)
        else:
            won = False

    context = {
        "lottery": lottery,
        "entered": entered,
        "won": won,
    }
    return render(request, "lotto/detail.html", context)
