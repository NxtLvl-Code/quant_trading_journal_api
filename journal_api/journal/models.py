from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True)
    bio = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Profile({self.user.username})"

class Tag(models.Model):
    tag_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.tag_name

class Trade(models.Model):
    SIDE_CHOICES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
        ('LONG', 'LONG'),
        ('SHORT', 'SHORT'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    asset_symbol = models.CharField(max_length=32)
    side = models.CharField(max_length=8, choices=SIDE_CHOICES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    trade_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, related_name='trades', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['asset_symbol'], name='ix_trades_symbol'),
            models.Index(fields=['user', 'created_at'], name='ix_trades_user_created'),
            # Note: Postgres partial index for soft deletes added via a migration below if desired.
        ]

    def __str__(self):
        return f"{self.asset_symbol} {self.side} {self.quantity or ''}@{self.price or ''}"
