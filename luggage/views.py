from django.http import JsonResponse
from .serializers import LuggageSerializer
from .models import Luggage
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def luggage_list(request) -> (JsonResponse | None):
    """ Get list of luggage types available """
    if request.method == 'GET':
        luggage_types = Luggage.objects.all()
        serializer = LuggageSerializer(luggage_types, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        request_body = json.loads(request.body)
        serializer = LuggageSerializer(data=request_body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
