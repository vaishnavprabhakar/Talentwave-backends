from company.models import Job
from rest_framework import serializers


class JobPostSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False)

    class Meta:
        model = Job
        exclude = ["user"]

    def create(self, validated_data):
        current_user = self.context["request"].user
        validated_data["user"] = current_user
        instance = super().create(validated_data)
        return instance

    def save(self, **kwargs):
        return super().save(**kwargs)
