from rest_framework import serializers

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)