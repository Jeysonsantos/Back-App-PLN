
from .resumir import resumir,stopwords
from .models import Texto
from rest_framework import viewsets
from .serializers import TextoSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

class TextoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Texto.objects.all()
    serializer_class = TextoSerializer

    def create(self, request):
        request.data['resumo'] = resumir(request.data['link'])
        serializer= TextoSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

