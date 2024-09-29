from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length = 50, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Service(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    img = models.ImageField(upload_to='service/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Rate(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.PositiveSmallIntegerField()
    txt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def each_service_rate(self):
        return Rate.objects.filter(servive=self.service).aggregate(average_rate=models.Avg('vote'))['vote']
    
    def __str__(self):
        return f"{self.service} {self.user}"
