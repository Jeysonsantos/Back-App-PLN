from rest_framework import serializers


class TextoSerializer(serializers.Serializer):
    link = serializers.URLField()
    resumo = serializers.CharField()
    
