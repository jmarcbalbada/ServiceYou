from django.shortcuts import render
from django.views import View
from django.db import connection
from .form import *
from django.shortcuts import HttpResponse

# Create your views here.



class PayFormView(View):
    template = 'payment.html'
    def get(self, request):
        pay = PayForm()
        return render(request, self.template, {'form': pay})

    def post(self, request):
        payHandler = PayForm(request.POST)

        if payHandler.is_valid():
            pay = payHandler.save(commit=False)

            with connection.cursor() as cursor:
                cursor.callproc('InsertPayment',[pay.requestID_id, pay.clientID_id,
                        pay.workerID_id, pay.amount, pay.paymentDate, pay.amountPaid,0 ])

            return render(request, self.template, {'form': pay})
        else:
            return  render(request,self.template,{'form':payHandler})