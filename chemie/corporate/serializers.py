from rest_framework import serializers
from .models import Interview, Specialization, JobAdvertisement


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name")
        model = Specialization


class InterviewSerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "text",
            "picture",
            "specializations",
            "is_published",
        )
        model = Interview


class JobAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = JobAdvertisement
