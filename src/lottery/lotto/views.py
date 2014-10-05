from django.shortcuts import render

from .models import Lottery


def list(request):
    lotteries = Lottery.objects.active().exclude(entrants=request.user)
    context = {
        "lotteries": lotteries,
    }
    return render(request, "lotto/list.html", context)
