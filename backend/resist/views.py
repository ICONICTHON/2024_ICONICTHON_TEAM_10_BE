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

sipal = "" 

@csrf_exempt
def select_classroom(request):
    if request.method == 'POST':
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)
            building_name = data.get('building_name')
            room_id = data.get('room_id')
            reservation_date = data.get('reservation_date')
            sipal = room_id
            # 필수 데이터 검증
            if not all([building_name, room_id, reservation_date]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Classroom 객체 생성 또는 가져오기
            classroom, created = Classroom.objects.get_or_create(
                room_id=room_id,
                defaults={
                    'building_name': building_name,
                    'room_id': room_id, 
                    'room_number': room_id,  # 필요에 따라 수정
                    'capacity': 99,  # 기본값 설정
                    'has_air_conditioning': False,  # 기본값 설정
                    'has_lighting': False  # 기본값 설정
                }
            )

            # 예약 객체 생성 (필요에 따라)
            # 여기서는 간단히 예약 날짜를 저장하는 것으로 가정
            # 이후 시간 남으면 해결해봄ㅋ
            reservation = Reservation.objects.create(
                classroom=classroom,
                reservation_date=reservation_date,
                # 다른 필드는 필요에 따라 추가
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=1),
                applicant=User.objects.first()  # 실제로는 적절한 사용자로 대체해야 함
            )

            return JsonResponse({'message': 'Reservation created successfully.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

@csrf_exempt
def select_classroom_1(request):
    if request.method == 'POST':# JSON 데이터 파싱
        data = json.loads(request.body)
        custom_tag = data.get('custom_tag')
        tag_1 = data.get('tag_1')
        tag_2 = data.get('tag_2')

    classroom = Classroom.objects.get(room_id=sipal)#room_id가 시팔인 데이터 긁어오기

    reservation = Reservation.objects.create(
                classroom=classroom,
                custum_tag=custom_tag,
                tag_1=tag_1,
                tag_2=tag_2,
                # 다른 필드들도 필요에 따라 추가
                applicant=User.objects.first(),  # 실제로는 적절한 User로 대체해야 함
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=1)
    )
    return JsonResponse({'message': 'Reservation created successfully.'}, status=201)

@csrf_exempt
def select_classroom_2(request):
    if request.method == 'GET':
        try:
            # 세션에서 room_id 가져오기
            room_id = request.session.get('room_id')
            if not room_id:
                return JsonResponse({'error': 'Room ID is not set in session.'}, status=400)

            # 해당 room_id의 가장 최근 Reservation 가져오기
            reservation = Reservation.objects.filter(classroom__room_id=room_id).order_by('-id').first()

            # 예약 정보가 없는 경우 처리
            if not reservation:
                return JsonResponse({'message': 'No reservations found for this room.'}, status=404)

            # 필요한 필드만 추출하여 JSON 생성
            response_data = {
                "Classroom": {
                    "building_name": reservation.classroom.building_name,
                    "room_id": reservation.classroom.room_id,
                    "reservation_date": reservation.reservation_date,
                    "start_time": reservation.start_time.strftime("%H:%M"),
                    "end_time": reservation.end_time.strftime("%H:%M"),
                    "custum_tag": reservation.custom_tag,
                    "tag_1": reservation.tag_1,
                    "tag_2": reservation.tag_2,
                }
            }

            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
    
@csrf_exempt
def start(request):
    return JsonResponse()