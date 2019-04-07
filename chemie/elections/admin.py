from django.contrib import admin

from .models import Candidate, Position, Election, Ticket

admin.site.site_header = "Valg"
admin.site.site_title = "Valg"

admin.site.register(Election)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["user", "get_position"]

    def get_position(self, obj):
        return "\n".join(obj.candidate_position.first().position_name)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "position", "get_candidates", "is_blank"]

    def get_candidates(self, obj):
        return "\n".join(
            [
                candidate.user.get_full_name() + ","
                for candidate in obj.candidates.all()
            ]
        )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_name",
        "spots",
        "total_votes",
        "blank_votes",
        "number_of_prevote_tickets",
        "is_active",
        "is_done",
        "get_candidates_votes",
    ]

    def get_candidates_votes(self, obj):
        return "\n".join(
            [
                candidate.user.get_full_name()
                + ": "
                + str(candidate.get_candidate_votes())
                + ","
                for candidate in obj.candidates.all()
            ]
        )

    def blank_votes(self, obj):
        return "\n".join(str(obj.get_blank_votes()))

    def total_votes(self, obj):
        return "\n".join(str(obj.get_total_votes()))
