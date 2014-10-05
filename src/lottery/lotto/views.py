from django.shortcuts import (
    get_object_or_404,
    redirect,
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
        if request.method == "POST":
            # We don't need any POST data for this, so we aren't using
            # a Django form.  Assuming if a POST that we are entering
            # the lottery.
            entered = True
            won = lottery.enter(request.user)
            return redirect(lottery.get_absolute_url())
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
