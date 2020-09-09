from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


class Auth:


    @staticmethod
    @csrf_exempt # TODO: for the purpose of testing 
    @require_http_methods(["POST"])
    def login_view(request):
        status = False
        msg = ""
        
        try:
            # A logged In User must logout before trying to login 
            assert request.user.is_authenticated is False
        
            user = authenticate(
                username=request.POST["username"], 
                password=request.POST["password"])

            if user:
                login(request, user)
                status, msg = True, "Logged In Successfully"
            else:
                raise Exception
        except Exception:
            status, msg = False, "Invalid Request"


        return JsonResponse({
            "status" : status,
            "msg" : msg
            })


    @staticmethod
    @require_http_methods(["POST"])
    @csrf_exempt # TODO: for the purpose of testing 
    def logout_view(request):

        status = False
        msg = ""

        if request.user.is_authenticated:
            logout(request)
            status, msg = True, "Logged Out!"
        else:
            status, msg = False, "Invalid Request"
    
        return JsonResponse({
            "status" : status,
            "msg" : msg
            })
