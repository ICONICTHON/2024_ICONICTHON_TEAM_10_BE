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
from .searializers import ClassroomSerializer
from datetime import datetime, timedelta

@csrf_exempt
def select_classroom(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name')
        room_id = request.POST.get('room_id')
        reservation_date = request.POST.get('reservation_date')
        
        # Convert reservation_date to a datetime object if it's provided as a string
        try:
            reservation_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Retrieve the classroom
        try:
            classroom = Classroom.objects.get(room_id=room_id, building_name=building_name)
        except Classroom.DoesNotExist:
            return JsonResponse({"error": "Classroom not found."}, status=404)
        
        # Retrieve reservations for the classroom on the specified date
        reservations = Reservation.objects.filter(
            classroom=classroom,
            reservation_date=str(reservation_date)
        ).order_by('start_time')
        
        # Determine available time slots (assuming 9 AM - 6 PM)
        start_time = datetime.combine(reservation_date, datetime.min.time()).replace(hour=9)
        end_time = start_time.replace(hour=18)
        
        # Calculate available times
        available_times = []
        current_time = start_time
        
        for reservation in reservations:
            if current_time < reservation.start_time:
                available_times.append({
                    "start": current_time.time().strftime('%H:%M'),
                    "end": (reservation.start_time - timedelta(minutes=1)).time().strftime('%H:%M')
                })
            current_time = max(current_time, reservation.end_time)
        
        # If there's still time left at the end of the day
        if current_time < end_time:
            available_times.append({
                "start": current_time.time().strftime('%H:%M'),
                "end": end_time.time().strftime('%H:%M')
            })
        
        return JsonResponse({"available_times": available_times}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def select_classroom(request):
    return JsonResponse()

@csrf_exempt
def search(request):
    return JsonResponse()

@csrf_exempt
def start(request):
    return JsonResponse()