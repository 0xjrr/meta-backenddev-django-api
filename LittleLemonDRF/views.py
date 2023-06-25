from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from .models import * # temporary, change at end
from .serializers import * # temporary, change at end
from .permissions import IsManager, IsCrew
import datetime

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

class ManagerGroupViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        group = Group.objects.get(name="manager")
        return group.user_set.all()

    # GET /api/groups/manager/users
    def list(self, request):
        group = get_object_or_404(Group, name="manager")
        serializer = self.serializer_class(group.user_set.all(), many=True)
        return Response(serializer.data)

    # POST /api/groups/manager/users
    def create(self, request):
        group = get_object_or_404(Group, name="manager")
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        group.user_set.add(user)
        return Response({'status': 'User added to manager group'}, status=status.HTTP_201_CREATED)
    # GET /api/groups/manager/users/{userId}
    def retrieve(self, request, pk=None):
        group = get_object_or_404(Group, name="manager")
        user = get_object_or_404(group.user_set, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # DELETE /api/groups/manager/users/{userId}
    def destroy(self, request, pk=None):
        group = get_object_or_404(Group, name="manager")
        user = get_object_or_404(User, pk=pk)
        group.user_set.remove(user)
        return Response({'status': 'User removed from manager group'}, status=status.HTTP_200_OK)

class DeliveryCrewGroupViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsCrew]

    def get_queryset(self):
        group = Group.objects.get(name="delivery_crew")
        return group.user_set.all()

    # GET /api/groups/delivery-crew/users
    def list(self, request):
        group = get_object_or_404(Group, name="delivery_crew")
        serializer = self.serializer_class(group.user_set.all(), many=True)
        return Response(serializer.data)

    # POST /api/groups/delivery-crew/users
    def create(self, request):
        group = get_object_or_404(Group, name="delivery_crew")
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        group.user_set.add(user)
        return Response({'status': 'User added to delivery-crew group'}, status=status.HTTP_201_CREATED)
    # GET /api/groups/delivery-crew/users/{userId}
    def retrieve(self, request, pk=None):
        group = get_object_or_404(Group, name="delivery_crew")
        user = get_object_or_404(group.user_set, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # DELETE /api/groups/delivery-crew/users/{userId}
    def destroy(self, request, pk=None):
        group = get_object_or_404(Group, name="delivery_crew")
        user = get_object_or_404(User, pk=pk)
        group.user_set.remove(user)
        return Response({'status': 'User removed from manager group'}, status=status.HTTP_200_OK)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        # If the user is a manager, return all orders
        if user.groups.filter(name="manager").exists():
            return Order.objects.all()

        # If the user is a delivery crew, return all orders for that delivery crew
        if user.groups.filter(name="delivery_crew").exists():
            return Order.objects.filter(delivery_crew=user)

        # If the user is a customer, return all orders for that customer
        if user.groups.filter(name="customer").exists():  # Customer
            return Order.objects.filter(user=user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        user = request.user

        if user.groups.filter(name="customer").exists():
            cart_items = Cart.objects.filter(user=user)
            
            if not cart_items.exists():
                return Response({'detail': 'No active cart found.'}, status=status.HTTP_400_BAD_REQUEST)
           
            total = cart_items.aggregate(
                total=models.Sum(models.F('menuitem__price') * models.F('quantity'), output_field=models.DecimalField())
            )['total']

            order = Order.objects.create(user=user, total=total, date=datetime.date.today())

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitem,
                    quantity=item.quantity
                )
            
            cart_items.delete()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response({'detail': 'Only customers can create orders.'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = request.user
        order = self.get_object()
        
        if user.groups.filter(name="manager").exists():
            serializer = self.get_serializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        
        if user.groups.filter(name="delivery_crew").exists() and 'status' in request.data:
            order.status = request.data['status']
            order.save()
            return Response(OrderSerializer(order).data)
        
        return Response({'detail': 'You do not have permission to update this order.'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        user = self.request.user
        if user.groups.filter(name="manager").exists():
            try:
                order = Order.objects.get(pk=pk)
                order.delete()
                return Response({'detail': 'Order has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
            except Order.DoesNotExist:
                return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'Only managers can delete orders.'}, status=status.HTTP_403_FORBIDDEN)
