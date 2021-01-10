from rest_framework import serializers
from .models import Candidate, Ticket, Position, Election
from chemie.customprofile.serializers import UserSerializer


class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Candidate
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)

    class Meta:
        model = Position
        fields = ("candidates", "position_name", "spots", "number_of_prevote_tickets",
                  "blank_votes", "is_active", "is_done", "by_acclamation")


class ElectionSerializer(serializers.ModelSerializer):
    current_position = PositionSerializer()

    class Meta:
        model = Election
        fields = "__all__"
