from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
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
        return Response({"message":"Updating an instance"}, status.HTTP_200_OK)
	
    def retrieve(self, request, pk=None):
        return Response({"message":"Displaying an instance"}, status.HTTP_200_OK)
	
    def partial_update(self, request, pk=None):
        return Response({"message":"Partially updating an instance"}, status.HTTP_200_OK)
	
    def destroy(self, request, pk=None):
        return Response({"message":"Deleting an instance"}, status.HTTP_200_OK)
