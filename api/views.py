from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from items.models import Item
from .serializers import ItemListSerializer, ItemDetailSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from .permissions import IsAddedBy

class ItemListView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    permission_classes = [AllowAny]
    filter_backend = [OrderingFilter, SearchFilter]
    search_fields = ['name', 'description']

class ItemDetailView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'
    # permission_classes = [IsAddedBy]

