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
            # 필수 데이터 검증
            global sipal
            sipal = room_id
            if not all([building_name, room_id, reservation_date]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            
            #json 데이터 출력
            print(f"building_name: {building_name}, room_id: {room_id}, reservation_date: {reservation_date}")
            # 여기에 대관 가능 여부 체크하는 코드 추가 
            
            # 

            # Classroom 객체 생성 또는 가져오기
            classroom, created = Classroom.objects.get_or_create(
                room_id=sipal,
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
'''
@csrf_exempt
def select_classroom_1(request):
    if request.method == 'POST':# JSON 데이터 파싱
        data = json.loads(request.body)
        custom_tag = data.get('custom_tag')
        tag_1 = data.get('tag_1')
        tag_2 = data.get('tag_2')


    reservation = Reservation.objects.create(
                classroom=classroom,
                custom_tag=custom_tag,
                tag_1=tag_1,
                tag_2=tag_2,
                # 다른 필드들도 필요에 따라 추가
                applicant=User.objects.first(),  # 실제로는 적절한 User로 대체해야 함
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=1)
    )
    return JsonResponse({'message': 'Reservation created successfully.'}, status=201)

@csrf_exempt
def select_classroom_1(request):
    if request.method == 'GET':
    
        '''
@csrf_exempt
def select_classroom_2(request):
     if request.method == 'POST':
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)
            
            # 받은 데이터 출력
            print("\n=== 받은 데이터 ===")
            print(data)
            
            # 데이터 추출
            building_name = data.get('building_name')
            room_id = data.get('room_id')
            reservation_date = data.get('reservation_date')
            start_time = data.get('start_time')
            custom_tag = data.get('custom_tag')
            tag1 = data.get('tag1')
            tag2 = data.get('tag2')

            # room_id가 없으면 전역 변수에서 가져오기
            if not room_id:
                global sipal
                room_id = sipal

            if not room_id:
                return JsonResponse({'error': 'Room ID is not set.'}, status=400)

            # 가장 최근에 생성된 해당 강의실의 Reservation 객체 가져오기
            reservation = Reservation.objects.filter(classroom__room_id=room_id).order_by('-id').first()
            if not reservation:
                return JsonResponse({'error': 'No reservation found for this room.'}, status=404)

            # 예약 정보 업데이트
            if start_time:
                reservation.start_time = datetime.strptime(f"{reservation_date} {start_time}", '%Y-%m-%d %H:%M')
            if custom_tag:
                reservation.custum_tag = custom_tag
            if tag1:
                reservation.tag_1 = tag1
            if tag2:
                reservation.tag_2 = tag2

            reservation.save()

            # 응답 데이터 구성
            response_data = {
                'building_name': reservation.classroom.building_name,
                'room_id': reservation.classroom.room_id,
                'reservation_date': reservation.start_time.strftime('%Y-%m-%d'),
                'start_time': reservation.start_time.strftime('%H:%M'),
                'custom_tag': reservation.custum_tag,
                'tag1': reservation.tag_1,
                'tag2': reservation.tag_2
            }

            print("\n=== 업데이트된 예약 정보 ===")
            print(response_data)

            return JsonResponse({
                'status': 'success',
                'message': 'Reservation updated successfully.',
                'data': response_data
            }, status=200)

        except json.JSONDecodeError as e:
            print(f"JSON 파싱 에러: {str(e)}")
            print(f"받은 데이터: {request.body}")
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

     return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


@csrf_exempt
def start(request):
    if request.method == 'POST':
        try:
            # 세션 또는 전역 변수에서 room_id 가져오기
            global sipal
            room_id = sipal
            if not room_id:
                return JsonResponse({'error': 'Room ID is not set.'}, status=400)

            # JSON 데이터 파싱
            data = json.loads(request.body)
            custum_tag = data.get('custum_tag')
            tag_1 = data.get('tag_1')
            tag_2 = data.get('tag_2')

            # 가장 최근에 생성된 해당 강의실의 Reservation 객체 가져오기
            reservation = Reservation.objects.filter(classroom__room_id=room_id).order_by('-id').first()
            if not reservation:
                return JsonResponse({'error': 'No reservation found for this room.'}, status=404)

            # 태그 업데이트
            reservation.custum_tag = custum_tag
            reservation.tag_1 = tag_1
            reservation.tag_2 = tag_2
            reservation.save()

            # 반환할 데이터 구성
            response_data = {
                'building_name': reservation.classroom.building_name,
                'room_id': reservation.classroom.room_id,
                'custum_tag': reservation.custum_tag,
                'tag_1': reservation.tag_1,
                'tag_2': reservation.tag_2,
            }

            return JsonResponse({'message': 'Reservation updated successfully.', 'reservation': response_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

@csrf_exempt
def get_unavailable_times(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            date_str = data.get('date')  # "YYYY-MM-DD" 형식

            if not all([room_id, date_str]):
                return JsonResponse({'error': 'Room ID and date are required.'}, status=400)

            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # 해당 날짜의 예약 및 강의 시간 조회
            reservations = Reservation.objects.filter(
                classroom__room_id=room_id,
                start_time__date=date
            )

            courses = Course.objects.filter(
                classroom__room_id=room_id,
                start_time__date=date
            )

            # 예약 및 강의 시간을 리스트로 변환
            unavailable_times = []
            for res in reservations:
                unavailable_times.append({
                    'start_time': res.start_time.strftime('%H:%M'),
                    'end_time': res.end_time.strftime('%H:%M'),
                })

            for course in courses:
                unavailable_times.append({
                    'start_time': course.start_time.strftime('%H:%M'),
                    'end_time': course.end_time.strftime('%H:%M'),
                })

            return JsonResponse({'unavailable_times': unavailable_times}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
