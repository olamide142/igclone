from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Account

class Register:


    @staticmethod
    @csrf_exempt # TODO: for the purpose of testing 
    @require_http_methods(["POST"])
    def register_user(request):
        
        user_exist = User.objects.filter(username=request.POST['username']).first()

        if (request.user.is_authenticated is False) and (user_exist is None):

            u = User.objects.create_user(
                username=request.POST['username'],
                email = request.POST['email'],
                password = request.POST['password']
            )
            u.save()

            a = Account(
                username=u.username,
                profile_name = u.username,
                bio = None
            )
            a.save()

            return JsonResponse({
                "status" : True,
                "msg" : "Account Created Successfully"
            }) 

        else:
            return JsonResponse({
                "status" : False,
                "msg" : "Invalid Request"
            })




    @staticmethod
    @csrf_exempt # TODO: for the purpose of testing 
    @require_http_methods(["POST"])
    def delete_profile(request):
        if request.user.is_authenticated:
            u = User.objects.get(username = request.user.username)
            u.delete()
            return JsonResponse({
                "status" : True,
                "msg" : "Account Deleted Successfully"
            })