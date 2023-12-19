from django.shortcuts import render
from django.db import connection
# Create your views here.

def acceptservice(request):
    cursor = connection.cursor()
    user_id = request.session.get('user_id')
    cursor.callproc('workerpendingrequest',[user_id])
    services = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        requestid = request.POST['requestid']
        status = request.POST['status']
        result = ''
        if status == 'cancelled':
            cursor = connection.cursor()
            cursor.callproc('canceltheservice', [user_id,requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()

        elif status == 'accepted':
            cursor = connection.cursor()
            cursor.callproc('acceptrequest', [user_id, requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()


        cursor = connection.cursor()
        cursor.callproc('workerpendingrequest', [user_id])
        services = cursor.fetchall()
        cursor.close()


        return render(request, 'acceptservice.html', {'services': services,'requestid':requestid,'result':result, 'status':status})
    elif request.method == "GET":
        return render(request, 'acceptservice.html', {'services': services})

def pendingservice(request):
    user_id = request.session.get('user_id')

    cursor = connection.cursor()
    cursor.callproc('pendingservice',[user_id])
    services = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        status = request.POST['status']
        requestid = ''
        result =''
        if status == 'whatfail':
            requestid = request.POST['requestid']
            cursor = connection.cursor()
            cursor.callproc('cancelthetransaction', [user_id,requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()

        if status == 'success':
            requestid = request.POST['requestid']
            cursor = connection.cursor()
            cursor.callproc('markcomplete', [user_id,requestid])
            result = cursor.fetchall()[0][0]
            cursor.close()

        cursor = connection.cursor()
        cursor.callproc('pendingservice', [user_id])
        services = cursor.fetchall()
        cursor.close()

        return render(request, 'pendingservice.html', {'services': services,'requestid':requestid,'result':result, 'status':status})
    elif request.method == "GET":
        return render(request, 'pendingservice.html', {'services': services})

def completedservice(request):
    user_id = request.session.get('user_id')

    cursor = connection.cursor()
    cursor.callproc('completedservice',[user_id])
    services = cursor.fetchall()
    cursor.close()
    return render(request, 'completedservice.html', {'services': services})

def failedservice(request):
    user_id = request.session.get('user_id')
    cursor = connection.cursor()

    cursor.callproc('failedservice',[user_id])
    services = cursor.fetchall()
    cursor.close()
    return render(request, 'failedservice.html', {'services': services})

def cancelledservice(request):
    cursor = connection.cursor()
    user_id = request.session.get('user_id')

    cursor.callproc('cancelledservice',[user_id])
    services = cursor.fetchall()
    cursor.close()
    return render(request, 'cancelledservice.html', {'services': services})
