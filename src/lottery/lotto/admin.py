from django.contrib import admin

from .models import Lottery


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    list_display = ("title", "active")
    prepopulated_fields = {"slug": ("title",)}
#    readonly_fields = ("winners",)
