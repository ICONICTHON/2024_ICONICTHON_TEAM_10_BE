# serializers.py
from rest_framework import serializers
from .models import User, Classroom, Reservation

# Reservation serializer
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['classroom', 'applicant', 'tag_1', 'tag_2', 'custum_tag', 'reservation_date', 'start_time', 'end_time']

# Classroom serializer
class ClassroomSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(write_only=True)  # 예약 정보를 포함

    class Meta:
        model = Classroom
        fields = ['room_id', 'room_number', 'building_name', 'capacity', 'reservation']

    def create(self, validated_data):
        # 예약 정보를 추출
        reservation_data = validated_data.pop('reservation')
        classroom = Classroom.objects.create(**validated_data)

        # 예약 생성
        Reservation.objects.create(classroom=classroom, **reservation_data)
        return classroom
