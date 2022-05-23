"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Game, Category, Player
from rest_framework.decorators import action
from django.db.models import Q


class GameView(ViewSet):
    """"Rater app game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()

        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

            Returns
            Response -- JSON serialized game instance
        """

        creator = Player.objects.get(user=request.auth.user)
        #category = Category.objects.get(pk=request.data['category_id'])
#Right is the server side left is what comes from the client
        game = Game.objects.create(
            title=request.data['title'],
            designer=request.data['designer'],
            description=request.data['description'],
            year_released=request.data['year_released'],
            number_of_players=request.data['number_of_players'],
            age_recomendations=request.data['age_recommendation'],
            estimated_time_to_play=request.data['estimated_time_to_play'],
            creator=creator

        )
        game.category.add(*request.data['category'])

        serializer = GameSerializer(game)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def add_category(self, request, pk):
        """Post request for a user to sign up for an event"""


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """

    class Meta:
        model = Game
        fields = ('id', 'title', 'designer', 'description', 'year_released', 'number_of_players',
                  'age_recomendations', 'estimated_time_to_play', "creator", "category")
        depth = 1
