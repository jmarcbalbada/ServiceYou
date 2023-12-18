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
        status = request.POST['status']
        result = ''
        if status == 'cancelled':
            cursor = connection.cursor()
            cursor.callproc('canceltheservice', [1,requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()

        elif status == 'accepted':
            cursor = connection.cursor()
            cursor.callproc('acceptrequest', [1, requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()


        cursor = connection.cursor()
        cursor.callproc('workerpendingrequest', [1])
        services = cursor.fetchall()
        cursor.close()


        return render(request, 'acceptservice.html', {'services': services,'requestid':requestid,'result':result, 'status':status})
    elif request.method == "GET":
        return render(request, 'acceptservice.html', {'services': services})

def pendingservice(request):
    cursor = connection.cursor()
    cursor.callproc('pendingservice',[1])
    services = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        status = request.POST['status']
        requestid = ''
        result =''
        if status == 'whatfail':
            requestid = request.POST['requestid']
            cursor = connection.cursor()
            cursor.callproc('cancelthetransaction', [1,requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()

        if status == 'success':
            requestid = request.POST['requestid']
            cursor = connection.cursor()
            cursor.callproc('markcomplete', [1,requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()

        cursor = connection.cursor()
        cursor.callproc('pendingservice', [1])
        services = cursor.fetchall()
        cursor.close()

        return render(request, 'pendingservice.html', {'services': services,'requestid':requestid,'result':result, 'status':status})
    elif request.method == "GET":
        return render(request, 'pendingservice.html', {'services': services})

def completedservice(request):
    cursor = connection.cursor()
    cursor.callproc('completedservice',[1])
    services = cursor.fetchall()
    cursor.close()
    return render(request, 'completedservice.html', {'services': services})

def failedservice(request):
    cursor = connection.cursor()
    cursor.callproc('failedservice',[1])
    services = cursor.fetchall()
    cursor.close()
    return render(request, 'failedservice.html', {'services': services})

def cancelledservice(request):
    cursor = connection.cursor()
    cursor.callproc('cancelledservice',[1])
    services = cursor.fetchall()
    cursor.close()
    return render(request, 'cancelledservice.html', {'services': services})
