from django.contrib import admin
from .models import Profile, Tag, Trade

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_name')
    search_fields = ('tag_name',)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'asset_symbol', 'side', 'quantity', 'price', 'trade_time')
    list_filter = ('side', 'asset_symbol')
    search_fields = ('asset_symbol', 'notes')
    autocomplete_fields = ('tags',)
