from django.db import models

# User model
class User(models.Model):
    student_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=10, choices=[('Admin', 'Admin'), ('Professor', 'Professor'), ('Student', 'Student')])
    is_returned = models.BooleanField(default=False)
		
    def __str__(self):
        return f"{self.name} ({self.student_id})"

# Classroom model
class Classroom(models.Model):
    room_id = models.CharField(max_length=50, primary_key=True)
    building_name = models.CharField(max_length=100, null=False, default = "신공학관")
    room_number = models.IntegerField(null=False)
    capacity = models.IntegerField(default=1)
    is_checked = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField()
    has_lighting = models.BooleanField()

    def __str__(self):
        return f"{self.building_name} {self.room_number}"

# Reservation model
class Reservation(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_1 = models.CharField(max_length=50, blank=True, null=True)
    tag_2 = models.CharField(max_length=50, blank=True, null=True)
    custum_tag = models.CharField(max_length=50, blank=True, null=True)
    reservation_date = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    attendees_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Reservation for {self.classroom} by {self.applicant}"

# Course model
class Course(models.Model):
    course_id = models.CharField(max_length=50, primary_key=True)
    course_name = models.TextField(max_length=50, blank=True, null=True)
    professor_name = models.TextField(max_length=50, blank=True, null=True)
    tag_1 = models.CharField(max_length=50, blank=True, null=True)
    tag_2 = models.CharField(max_length=50, blank=True, null=True)
    custum_tag = models.CharField(max_length=50, blank=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    def __str__(self):
        return f"Course {self.course_id} in {self.classroom}"