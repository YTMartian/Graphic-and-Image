from django.contrib import admin
from .models import Teacher, Student, Course, Examination, StuExam, Grade, Location


class TeacherAdmin(admin.ModelAdmin):
    list_filter = ('teacherId', 'Name')
    list_display = ('teacherId', 'Name', 'Gender', 'Major', 'Password')
    list_per_page = 20
    search_fields = ('teacherId', 'Name')


class StudentAdmin(admin.ModelAdmin):
    list_filter = ('studentId', 'Name')
    list_display = ('studentId', 'Name', 'Gender', 'Major', 'Class', 'Password')
    list_per_page = 20
    search_fields = ('studentId', 'Name')


class CourseAdmin(admin.ModelAdmin):
    list_filter = ('courseId', 'Name')
    list_display = ('courseId', 'Name', 'Teacher', 'Attribute', 'Hour', 'Class', 'Credit', 'Term', 'StartEndWeek')
    list_per_page = 20
    search_fields = ('courseId', 'Name')


class ExaminationAdmin(admin.ModelAdmin):
    list_filter = ('courseId', 'courseName')
    list_display = (
        'courseId', 'courseName', 'Start', 'End', 'Class', 'Amount', 'Location', 'Term', 'Teacher', 'TeacherAmount',
        'ApplyState', 'ExamState', 'PrimaryTeacher')
    list_per_page = 20
    search_fields = ('courseId', 'courseName')


class StuExamAdmin(admin.ModelAdmin):
    list_filter = ('stuId', 'stuName', 'courseName')
    list_display = (
        'stuId', 'stuName', 'courseId', 'courseName', 'Major', 'Start', 'End', 'Location', 'Teacher', 'TeacherAmount',
        'Term')
    list_per_page = 20
    search_fields = ('stuId', 'stuName', 'courseName')


class GradeAdmin(admin.ModelAdmin):
    list_filter = ('stuId', 'stuName', 'courseName')
    list_display = ('stuId', 'stuName', 'courseId', 'courseName', 'Credit', 'Attribute', 'GradePoint', 'UsuallyGrade',
                    'ExperimentGrade', 'FinalGrade')
    list_per_page = 20
    search_fields = ('stuId', 'stuName', 'courseName')


class LocationAdmin(admin.ModelAdmin):
    list_filter = ('LocationId', 'Place')
    list_display = ('LocationId', 'Place', 'Amount')
    list_per_page = 20
    search_fields = ('LocationId', 'Place')


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(StuExam, StuExamAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Location, LocationAdmin)