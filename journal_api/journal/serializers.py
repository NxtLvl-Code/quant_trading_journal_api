from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Tag, Trade

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']

class TradeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, required=False, source='tags'
    )

    class Meta:
        model = Trade
        fields = [
            'id', 'user', 'asset_symbol', 'side', 'quantity', 'price',
            'trade_time', 'notes', 'deleted_at', 'tags', 'tag_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'timezone']
