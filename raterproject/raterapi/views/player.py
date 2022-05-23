"""View module for handling requests about game types"""
from urllib import request
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Player


class PlayerView(ViewSet):

    def list(self, request):
        player = Player.objects.get(user=request.auth.user)

        serializer = PlayerSerializer(player)
        return Response(serializer.data)


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews"""
    class Meta:
        model = Player
        fields = ('id', 'user_id')
        depth = 1
