from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.db import connection
from .form import *


# Create your views here.

def registration(request):
    return HttpResponse("Register page")


def homePage(request):
    return HttpResponse("Home page")


class HomePageView(View):
    template = 'home.html'

    # registerRedirect = 'registerpage'
    # loginRedirect = 'login'

    def get(self, request):
        # Retrieve user_id from the session
        user_id = request.session.get('user_id')

        # Now you can use user_id in your view logic
        if user_id:
            # Retrieve the user object using the user_id
            user = Worker.objects.get(pk=user_id)

            # Pass the username to the template
            firstname = user.firstName if user else None

            cursor = connection.cursor()
            query = (
                'SELECT COUNT(*) FROM account_postservice WHERE '
                'workerID_id = %s AND is_active = 1'
            )
            cursor.execute(query, [user_id])
            transaction_count = cursor.fetchone()[0]
            cursor.close()

            # Render the template with the username
            return render(request, self.template, {'firstname': firstname, 'transaction_count': transaction_count})
        else:
            # User is not logged in, handle accordingly
            return render(request, self.template, {'username': None})


class PostServiceWorker(View):
    template = 'postserviceworker.html'

    def get(self, request):
        postService = PostServiceForm()
        user_id = request.session.get('user_id')
        user = Worker.objects.get(pk=user_id)
        post_worker_id = user.workerID
        print(post_worker_id)
        return render(request, self.template, {'form': postService})

    def post(self, request):
        postServiceForm = PostServiceForm(request.POST)
        user_id = request.session.get('user_id')
        user = Worker.objects.get(pk=user_id)
        post_worker_id = user.workerID
        print(post_worker_id)
        if postServiceForm.is_valid():
            # Assuming you have a model named PostService
            postService = postServiceForm.save(commit=False)

            # Execute the stored procedure
            with connection.cursor() as cursor:
                cursor.callproc('insertPostService',
                                [post_worker_id, postService.serviceID, postService.title,
                                 postService.description, postService.location, postService.date_posted,
                                 1, 0])

            return redirect('querypostservice')
        else:
            return render(request, self.template, {'form': postServiceForm})


class QueryPostServiceView(View):
    template_name = 'querypostservice.html'

    def get(self, request):
        # with connection.cursor() as cursor:
        # cursor.callproc('queryPostService', [1])  # Assuming 1 is a sample workerID parameter
        user_id = request.session.get('user_id')
        cursor = connection.cursor()
        query = 'SELECT postID, title, description, location, workerID_id, serviceID_id FROM account_postservice WHERE workerID_id = %s AND is_active = 1'
        cursor.execute(query, [user_id])
        postServices = cursor.fetchall()
        cursor.close()
        print(postServices)

        context = {'postServices': postServices}
        return render(request, self.template_name, context)


class DeletePostService(View):
    template = 'deletepostservice.html'

    def get(self, request):
        user_id = request.session.get('user_id')
        # Using Django ORM to fetch post services
        post_services = PostService.objects.filter(workerID_id=user_id, is_active=1).values('postID', 'title')

        context = {'postServices': post_services}
        return render(request, self.template, context)

    def post(self, request):
        post_id = request.POST.get('postID')

        with connection.cursor() as cursor:
            # Call the stored procedure
            cursor.callproc('softDeletePostServiceByPostID', [post_id, None])
            cursor.execute("SELECT @p_isDeleted")
            is_deleted = cursor.fetchone()[0]

        if is_deleted:
            messages.success(request, f"PostService with ID {post_id} deleted successfully.")
        else:
            messages.error(request, f"Failed to delete PostService with ID {post_id}.")

        return redirect('querypostservice')

        # with connection.cursor() as cursor:
        #     # Call the stored procedure
        #     cursor.callproc('softDeletePostServiceByPostID', [post_id, None])
        #     cursor.execute("SELECT @p_isDeleted")
        #     is_deleted = cursor.fetchone()[0]
        #
        # if is_deleted:
        #     messages.success(request, f"PostService with ID {post_id} deleted successfully.")
        # else:
        #     messages.error(request, f"Failed to delete PostService with ID {post_id}.")

        # return redirect('querypostservice')


class UpdatePostService(View):
    template = 'updatepostservice.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('postID')

        # Retrieve post details from the database
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT postID, title, description, location, serviceID_id FROM account_postservice WHERE postID = %s',
                [post_id]
            )
            post_details = cursor.fetchone()

        # Check if the post with the specified postID exists
        if not post_details:
            return HttpResponseNotFound("Post not found")

        # Create a form with initial data from the post details
        form = PostServiceForm(initial={
            'postID': post_details[0],
            'title': post_details[1],
            'description': post_details[2],
            'location': post_details[3],
            'serviceID': post_details[4],
        })

        return render(request, self.template, {'form': form, 'postID': post_id})

    def post(self, request, *args, **kwargs):
        # Access the postID parameter
        post_id = kwargs.get('postID')

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT postID, title, description, location, serviceID_id FROM account_postservice WHERE postID = %s',
                [post_id]
            )
            post_details = cursor.fetchone()

        if not post_details:
            return HttpResponseNotFound("Post not found")

        # Create a form instance and populate it with data from the request
        form = PostServiceForm(request.POST)

        # Validate the form
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE account_postservice SET title = %s, description = %s, location = %s, serviceID_id = %s '
                    'WHERE postID = %s',
                    [form.cleaned_data['title'], form.cleaned_data['description'], form.cleaned_data['location'], form.cleaned_data['serviceID'],
                     post_id]
                )

            return redirect('querypostservice')
        else:
            return render(request, self.template, {'form': form, 'postID': post_id})


# class RegisterWorker(View):
#     template = 'register.html'
#     nextPageTemplate = 'login.html'
#
#     def get(self, request):
#         worker = RegisterForm()
#         return render(request, self.template, {'form': worker})
#
#     def post(self, request):
#         worker = RegisterForm(request.POST)
#         if worker.is_valid():
#             worker.save()
#             # proceed to login page
#             return HttpResponseRedirect(reverse('login'))
#         else:
#             # Something went wrong
#             messages.error(request, 'Something went wrong. Please try again.')
#             return render(request, self.template, {'form': worker})


# class LoginWorker(View):
#     template = 'login.html'
#
#     def get(self, request):
#         worker = LoginForm()
#         return render(request, self.template, {'form': worker})
#
#     def post(self, request):
#         worker = LoginForm(request.POST)
#         if worker.is_valid():
#             worker_id = worker.cleaned_data.get('worker_id')
#             password = worker.cleaned_data.get('password')
#
#             User = get_user_model()
#
#             try:
#                 worker = User.objects.get(workerId=worker_id)
#             except User.DoesNotExist:
#                 worker = None
#
#             if worker is not None and worker.check_password(password):
#                 # Authentication was successful, so log in the user
#                 login(request, worker)
#                 # Redirect to a success page or the user's profile page
#                 return HttpResponseRedirect(reverse('profile'))  # Replace 'profile' with your desired URL name
#             else:
#                 # Authentication failed, show an error message
#                 messages.error(request, 'Invalid worker ID or password.')
#         else:
#             # Form validation failed, show an error message
#             messages.error(request, 'Please correct the form errors.')
#
#         return render(request, self.template, {'form': worker})

# class LoginWorker(View):
#     template = 'login.html'
#
#     def get(self, request):
#         worker = LoginForm()
#         return render(request, self.template, {'form': worker})
#
#     def post(self, request):
#         worker = LoginForm(request.POST)
#         if worker.is_valid():
#             worker.save()
#             # proceed to login page
#             return render(request, self.template, {'form': worker})
#         else:
#             # Something went wrong
#             return render(request, self.template, {'form': worker})
