from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Teacher(models.Model):
    teacherId = models.CharField('职工号', max_length = 20, blank = False)
    Name = models.CharField('姓名', max_length = 100, blank = False)
    Gender = models.CharField('性别', max_length = 10, blank = False)
    Birth = models.DateField('出生日期', auto_now_add = False)
    Major = models.CharField('院系', max_length = 100, blank = False)
    Password = models.CharField('密码', max_length = 100, blank = False)
    
    def __str__(self):
        return self.teacherId
    
    class Meta:
        ordering = ['-teacherId']


class Student(models.Model):
    studentId = models.CharField('学号', max_length = 20, blank = False)
    Name = models.CharField('姓名', max_length = 100, blank = False)
    Gender = models.CharField('性别', max_length = 10, blank = False)
    Birth = models.DateField('出生日期', auto_now_add = False)
    Major = models.CharField('院系', max_length = 100, blank = False)
    Class = models.CharField('班级', max_length = 100, blank = False)
    Password = models.CharField('密码', max_length = 100, blank = False)
    
    def __str__(self):
        return self.studentId
    
    class Meta:
        ordering = ['-studentId']


class Course(models.Model):
    courseId = models.CharField('课程号', max_length = 20, blank = False)
    Name = models.CharField('课程名', max_length = 100, blank = False)
    Teacher = models.CharField('授课教师', max_length = 100, blank = False)
    Attribute = models.CharField('属性', max_length = 100, blank = False)
    Hour = models.FloatField('学时', blank = False)
    Class = models.CharField('班级', max_length = 100, blank = False)
    Credit = models.FloatField('学分', blank = False)
    Term = models.CharField('学期', max_length = 20, blank = False)
    StartEndWeek = models.CharField('起始周', max_length = 20, blank = False)
    
    def __str__(self):
        return self.courseId
    
    class Meta:
        ordering = ['-courseId']


class Examination(models.Model):
    courseId = models.CharField('课程号', max_length = 20, blank = False)
    courseName = models.CharField('课程名', max_length = 100, blank = False)
    Start = models.DateTimeField('开始时间', blank = False)
    End = models.DateTimeField('结束时间', blank = False)
    Class = models.CharField('班级', max_length = 100, blank = False)
    Amount = models.IntegerField('人数', blank = False)
    Location = models.CharField('地点', max_length = 100, blank = False)
    Term = models.CharField('学期', max_length = 20, blank = False)
    Teacher = models.CharField('监考教师', max_length = 100, blank = False)
    TeacherAmount = models.IntegerField('监考老师人数', blank = False)
    ApplyState = models.BooleanField("申请状态", default = False, blank = False)
    ExamState = models.BooleanField("考试状态", default = False, blank = False)
    PrimaryTeacher = models.CharField('主考教师', max_length = 100, default = '', blank = False)
    
    def __str__(self):
        return self.courseId
    
    class Meta:
        ordering = ['-courseId']


class StuExam(models.Model):
    stuId = models.CharField('学号', max_length = 20, blank = False)
    stuName = models.CharField('姓名', max_length = 100, blank = False)
    courseId = models.CharField('课程号', max_length = 20, blank = False)
    courseName = models.CharField('课程名', max_length = 100, blank = False)
    Major = models.CharField('专业', max_length = 100, blank = False)
    Start = models.DateTimeField('开始时间', blank = False)
    End = models.DateTimeField('结束时间', blank = False)
    Location = models.CharField('地点', max_length = 100, blank = False)
    Teacher = models.CharField('监考教师', max_length = 100, blank = False)
    TeacherAmount = models.IntegerField('监考老师人数', blank = False)
    Term = models.CharField('学期', max_length = 100, blank = False)
    
    def __str__(self):
        return self.stuId
    
    class Meta:
        ordering = ['-stuId']


class Grade(models.Model):
    stuId = models.CharField('学号', max_length = 20, blank = False)
    stuName = models.CharField('姓名', max_length = 100, blank = False)
    courseId = models.CharField('课程号', max_length = 20, blank = False)
    courseName = models.CharField('课程名', max_length = 100, blank = False)
    Credit = models.FloatField('学分', blank = False)
    Attribute = models.CharField('属性', max_length = 100, blank = False)
    GradePoint = models.FloatField('绩点', blank = False)
    UsuallyGrade = models.FloatField('期末成绩', blank = False)
    ExperimentGrade = models.FloatField('平时成绩', blank = False)
    FinalGrade = models.FloatField('最终成绩', blank = False)
    
    def __str__(self):
        return self.stuId
    
    class Meta:
        ordering = ['-stuId']


class Location(models.Model):
    LocationId = models.CharField('考场号', max_length = 20, blank = False)
    Place = models.CharField('地点', max_length = 100, blank = False)
    Amount = models.IntegerField('人数', blank = False)
    
    def __str__(self):
        return self.LocationId
    
    class Meta:
        ordering = ['-LocationId']