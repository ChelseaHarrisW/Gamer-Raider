"""View module for handling requests about game types"""
from urllib import request
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Review, Game, Player


class ReviewView(ViewSet):
    """Rater app Review view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single Review
        
        Returns:
            Response -- JSON serialized Review
        """
        
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all reviews
        
        Returns:
            Response -- JSON serialized list of reviews
        """
        reviews = Review.objects.all()
        
        game = request.query_params.get('game', None)
        if game is not None:
            reviews = reviews.filter(game_id = game)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized review instance
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game_id'])
    
        review = Review.objects.create(
            content=request.data["content"],
            game = game,
            player = player
        )
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    
    
    
    
    
    
class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews"""
    class Meta:
        model = Review
        fields = ('id', 'content', 'game', 'player')
        depth = 2