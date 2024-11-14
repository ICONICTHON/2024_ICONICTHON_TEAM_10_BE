from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework import generics
from .models import Classroom, User, Reservation, Course

# Create your views here.

'''
@csrf_exempt
class ClassroomReservationCreateView(APIView):
    def post(self, request):
        #serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def professor_classroom(request):
    return JsonResponse()

@csrf_exempt
def select_classroom(request):
    return JsonResponse()

@csrf_exempt
def search(request):
    return JsonResponse()

@csrf_exempt
def start(request):
    return JsonResponse()

    '''