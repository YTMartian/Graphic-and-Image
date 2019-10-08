from django.db import models


class User(models.Model):
    name = models.CharField('用户名', max_length = 20, blank = False)
    password = models.CharField('密码', max_length = 100, blank = False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-name']


class History(models.Model):
    name = models.CharField('用户名', max_length = 20, blank = False)
    time = models.DateTimeField('时间', auto_now = False, blank = False)
    photograph = models.CharField('图片', max_length = 100, blank = False)
    license_plate = models.CharField('车牌号', max_length = 100, blank = False)
    type = models.CharField('车型', max_length = 10, blank = False)
    state = models.BooleanField('状态', default = False, blank = False)  # True代表离开，收费字段填入金额
    price = models.FloatField('收费', blank = True, default = 0.0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-name']


class UserPlate(models.Model):
    name = models.CharField('用户名', max_length = 20, blank = False)
    license_plate = models.CharField('车牌号', max_length = 100, blank = False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-name']