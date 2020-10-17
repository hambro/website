from rest_framework import serializers
from .models import Candidate, Ticket, Position, Election
from chemie.customprofile.serializers import UserSerializer


class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Candidate
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class ElectionSerializer(serializers.ModelSerializer):
    current_position = PositionSerializer()

    class Meta:
        model = Election
        fields = "__all__"
