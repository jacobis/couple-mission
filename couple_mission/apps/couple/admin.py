from django.contrib import admin

# Project
from couple_mission.apps.couple.models import Couple, CoupleBadge, CoupleTitle, CoupleDday
from couple_mission.apps.uai.models import Badge, Title


class AdminCouple(admin.ModelAdmin):
    list_display = ('id', 'partner_a', 'partner_b')


class AdminBadge(admin.ModelAdmin):
    list_display = ('id', 'badge', 'status')


class AdminTitle(admin.ModelAdmin):
    list_display = ('id', 'title', 'status')


class AdminDday(admin.ModelAdmin):
    list_display = ('id', 'title', 'date')

admin.site.register(Couple, AdminCouple)
admin.site.register(CoupleBadge, AdminBadge)
admin.site.register(CoupleTitle, AdminTitle)
admin.site.register(CoupleDday, AdminDday)
