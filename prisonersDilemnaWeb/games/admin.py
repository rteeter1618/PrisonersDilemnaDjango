from django.contrib import admin

from games.models import Game, MatchSummary, Player

# Register your models here.


class PlayerAdmin(admin.ModelAdmin):
    list_display=['name', 'user']

admin.site.register(Player, PlayerAdmin)
admin.site.register(Game)
