from rest_framework.decorators import api_view
from .resumir import resumir
from rest_framework import viewsets
from .serializers import TextoSerializer
from rest_framework.response import Response

class TextoViewSet(viewsets.GenericViewSet):
    queryset=[]
@api_view(['post'])

def create(request):
    request.data['resumo'] = resumir(request.data['link'])
    serializer= TextoSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors)



    