from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import * # temporary, change at end
from .serializers import * # temporary, change at end


class MenuItems(viewsets.ViewSet):

    def list(self, request):
        queryset = MenuItem.objects.all()
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = MenuItem.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = MenuItem.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = MenuItem.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data, partial=True) # Set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = MenuItem.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        menuitem_id = request.data.get('menuitem')
        quantity = request.data.get('quantity', 1)

        if quantity < 0:
            return Response({'error': 'Quantity cannot be negative'}, status=400)

        if menuitem_id is not None:
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                menuitem_id=menuitem_id,
                defaults={'quantity': quantity},
            )

            if quantity == 0:
                cart_item.delete()
                return Response(status=204)

            if not created:
                cart_item.quantity = quantity
                cart_item.save()

            serializer = CartSerializer(cart_item, context={'request': request})
            return Response(serializer.data, status=201 if created else 200)

        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=204)