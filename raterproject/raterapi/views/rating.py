"""View module for handling requests about game types"""
from urllib import request
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Rating, Game, Player

class RatingView(ViewSet):
    """Rater app Rating view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single Rating
        
        Returns:
            Response -- JSON serialized Rating
        """
        
        try:
            Rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(Rating)
            return Response(serializer.data)
        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all Ratings
        
        Returns:
            Response -- JSON serialized list of Ratings
        """
        ratings = Rating.objects.all()
        
        game = request.query_params.get('game', None)
        if game is not None:
            ratings = ratings.filter(game_id = game)
        
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized Rating instance
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game_id'])
    
        rating = Rating.objects.create(
            rating=request.data["rating"],
            game = game,
            player = player
        )
        
        serializer = RatingSerializer(rating)
        return Response(serializer.data)
    
    
    
    
    
    
    
class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for Ratings"""
    class Meta:
        model = Rating
        fields = ('id', 'rating', 'game', 'player')