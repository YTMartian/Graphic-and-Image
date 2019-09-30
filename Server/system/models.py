from django.db import models


class Test(models.Model):
    id = models.CharField('id', max_length = 20, blank = False, primary_key = True)
    num = models.CharField('值', max_length = 100, blank = False)
    
    def __str__(self):
        return self.id
    
    class Meta:
        ordering = ['-id']