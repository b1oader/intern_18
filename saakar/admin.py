from django.contrib import admin
from .models import Type, Hero, Fight


class FightAdmin(admin.ModelAdmin):
    # editable in adding, readonly in edit
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['hero_1', 'hero_2', 'result', 'fight_date', 'kill_loser']
        else: 
            return []


admin.site.register(Type)
admin.site.register(Hero)
admin.site.register(Fight, FightAdmin)
