from django.utils import timezone
from django.db import models


#  Create your models here.
# [Marc] - implemented 7 tables Client, Worker, Service, ServiceRequest, Payment, RateService, PostService
# Will be calling Customer -> Client

class Client(models.Model):
    clientID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=10)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    phoneNo = models.CharField(max_length=11)
    email = models.EmailField()

    def __str__(self):
        return str(self.clientID)

    @classmethod
    def authenticate_client(cls, username, password):
        # Your authentication logic for the Client model
        try:
            user = cls.objects.get(username=username, password=password)
            return user
        except cls.DoesNotExist:
            return None


class Worker(models.Model):
    workerID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=10)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    phoneNo = models.CharField(max_length=11)
    email = models.EmailField()

    def __str__(self):
        return str(self.workerID)

    @classmethod
    def authenticate_worker(cls, username, password):
        # Your authentication logic for the Worker model
        try:
            user = cls.objects.get(username=username, password=password)
            return user
        except cls.DoesNotExist:
            return None


class Service(models.Model):
    serviceID = models.AutoField(primary_key=True)
    serviceName = models.CharField(max_length=49)
    description = models.CharField(max_length=199)

    def __str__(self):
        return str(self.serviceID)


class ServiceRequest(models.Model):
    requestID = models.AutoField(primary_key=True)
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE)
    workerID = models.ForeignKey(Worker, on_delete=models.CASCADE)
    serviceID = models.ForeignKey(Service, on_delete=models.CASCADE)
    requestDate = models.DateField()
    SERVICE_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=SERVICE_STATUS_CHOICES, default='Pending')
    dateAccepted = models.DateField(null=True, blank=True)
    dateFinished = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.requestID)


class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    requestID = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE)
    workerID = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField()
    paymentDate = models.DateField()
    amountDue = models.FloatField(default=0.0,editable= False)
    amountPaid = models.FloatField()
    PAYMENT_STATUS = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Ongoing',editable=False)

    def __str__(self):
        return str(self.paymentID)


class RateService(models.Model):
    rateID = models.AutoField(primary_key=True)
    requestID = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    rateValue = models.IntegerField()
    comment = models.TextField(max_length=500)

    def __str__(self):
        return str(self.rateID)


class PostService(models.Model):
    postID = models.AutoField(primary_key=True)
    workerID = models.ForeignKey(Worker, on_delete=models.CASCADE)
    serviceID = models.ForeignKey(Service, on_delete=models.CASCADE)

    # Additional attributes
    title = models.CharField(default="",max_length=100, help_text="Title of the service post")
    description = models.TextField(default="", help_text="Description of the service")
    location = models.CharField(default="", max_length=255)
    date_posted = models.DateTimeField(default=timezone.now, help_text="Date and time when the post was created")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Post ID: {self.postID}, Title: {self.title}, Worker: {self.workerID}, Service: {self.serviceID}"