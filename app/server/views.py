from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .schema import server_list_docs
from .serializer import ServerSerializer
from .models import ServerModel

@server_list_docs
class ServerListViewSet(viewsets.ViewSet):

    queryset = ServerModel.objects.all()

    def list (self, request):
        """category from ServerModel"""
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == 'true'
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == 'true'

        #if by_user and not request.user.is_authenticated:
            #raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name=category)
        
        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        """Quantity of servers returned"""
        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValueError(detail=f"Server value error")

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)