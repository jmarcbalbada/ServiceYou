from django.shortcuts import render
from django.db import connection
# Create your views here.


def acceptservice(request):
    cursor = connection.cursor()
    cursor.callproc('workerpendingrequest',[11])
    services = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        requestid = request.POST['requestid']
        cursor = connection.cursor()
        result = 'nganung gwapo si winson'
        cursor.callproc('acceptrequest', [11,requestid,result])
        cursor.close()
        # services = cursor.fetchall()
        return render(request, 'acceptservice.html', {'services': services,'requestid':requestid,'result':result})
    return render(request, 'acceptservice.html', {'services': services})
