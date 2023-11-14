from rest_framework import serializers
from authentication.models import User



class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')



