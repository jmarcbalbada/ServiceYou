from django.shortcuts import render
from django.db import connection
# Create your views here.


def acceptservice(request):
    cursor = connection.cursor()
    cursor.callproc('workerpendingrequest',[1])
    services = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        requestid = request.POST['requestid']
        cursor = connection.cursor()
        result = 'nganung gwapo si winson'
        cursor.callproc('acceptrequest', [1,requestid,result])
        cursor.close()

        return render(request, 'acceptservice.html', {'services': services,'requestid':requestid,'result':result})
    elif request.method == "GET":
        return render(request, 'acceptservice.html', {'services': services})
