from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from api.models import Account as Account_DB
from api.services.follows import Follows as FS
from .tools import Tools

class Account:




    @staticmethod
    @require_http_methods(["GET"])
    def view_account(request, username):
        """
        Load the information about an account
        :param request: HttpRequest request
        :param username: User.username
        :return: JsonResponse
        """
        status, msg, bio, profile_name, follows, no_of_post, block_status, is_private =\
            False,"Invalid Request",None,None,None,None,None,None

        if not request.user.is_authenticated:
            return JsonResponse({"status":status, "msg":msg})
        account = Account_DB.objects.filter(username=username).first()

        if account is not None:
            each_other_status = FS.each_other_status(request.user.username, username)
            if each_other_status[request.user.username+"blocked"] == "1":
                block_status = {"status" : True, "msg" : f"Unblock {username} to view his/she profile"}
            elif each_other_status[username+"blocked"] == "1":
                block_status = {"status" : True, "msg" : f"{username} has blocked you from viewing his/her profile"}
            else:
                block_status = {"status" : False, "msg" : None}
                if account.is_private and (each_other_status[request.user.username + "follows"] == "0"):
                    is_private = {"status" : True, "msg" : "Send a Follow Request"}
            follows_count = FS.get_follows_count(username)
            status, msg, bio, profile_name, follows, no_of_post, block_status, is_private = \
                True, "Success", account.bio, account.profile_name, follows_count, None, block_status, is_private
        else:
            status, msg = False, "profile does not exist"

        return JsonResponse({
            "status":status, "msg":msg, "bio":bio, "profile_name":profile_name, "post_count":0, "follows" : follows_count,
            "block_status":block_status, "is_private":is_private
        })



    @staticmethod
    @require_http_methods(['POST']) #PUT was buggy
    def update_account(request,username):
        """
        Update personal details
        :param request: HttpRequest
        :return: JsonResponse
        """
        status, msg = False, "Invalid Request"

        if request.user.is_authenticated:
            user = request.user
            a = Account_DB.objects.filter(username=user.username).first()
            # Update Account Model
            a.profile_name = request.POST['profile_name']
            a.bio = request.POST['bio']
            a.save()
            # Update email
            email = request.POST["email"]
            if Tools.is_email_valid(email) or (email == user.email):
                user.email = email
                user.save()
            else:
                status, msg = False, "An account with this email already exist"
        return JsonResponse({"status":status, "msg":"Profile Updated Successfully"})

