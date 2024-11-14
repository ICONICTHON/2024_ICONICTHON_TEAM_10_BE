from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from resist.models import Classroom, Reservation

@csrf_exempt
def search_studyroom(request):
    if request.method == 'POST':
        try:
            # POST 데이터 파싱
            building_name = request.POST.get('building_name', '')
            room_number = request.POST.get('room_number', '')
            tag_1 = request.POST.get('tag_1', '')
            tag_2 = request.POST.get('tag_2', '')

            # 기본 쿼리: tag_1이 'studyroom'인 예약
            query = Q(tag_1='studyroom')
            
            # 추가 검색 조건
            if building_name:
                query &= Q(classroom__building_name__icontains=building_name)
            if room_number:
                query &= Q(classroom__room_number=room_number)
            if tag_2:
                query |= Q(tag_2__icontains=tag_2)

            # 예약 정보 조회
            reservations = Reservation.objects.filter(query).select_related('classroom')

            # 결과를 JSON 형식으로 변환
            results = []
            for reservation in reservations:
                results.append({
                    'room_id': reservation.classroom.room_id,
                    'building_name': reservation.classroom.building_name,
                    'room_number': reservation.classroom.room_number,
                    'capacity': reservation.classroom.capacity,
                    'tag_1': reservation.tag_1,
                    'tag_2': reservation.tag_2,
                    'reservation_date': reservation.reservation_date,
                    'start_time': reservation.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': reservation.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                })

            return JsonResponse({
                'status': 'success',
                'count': len(results),
                'data': results
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# Create your views here.