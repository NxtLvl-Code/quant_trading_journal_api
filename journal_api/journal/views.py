from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Profile, Tag, Trade
from .serializers import ProfileSerializer, TagSerializer, TradeSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('tag_name')
    serializer_class = TagSerializer

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all().order_by('-trade_time', '-created_at')
    serializer_class = TradeSerializer

    def destroy(self, request, *args, **kwargs):
        # Soft delete: set deleted_at, don't actually delete
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save(update_fields=['deleted_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer
