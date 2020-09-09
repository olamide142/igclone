"""
Validate Request that i really should not create classes for
- username is available
- password is valid
- email is available
-
"""

from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Account as Account_DB
import json

class Tools:

    @staticmethod
    def is_username_valid(username):
        """
        Check if a username follows requirements
        and username is not taken
        :param username: str
        :return: bool
        """
        user = User.objects.filter(username=username).first()
        if user is None:
            return True
        else:
            return False

    @staticmethod
    def is_password_valid(password):
        """
        Check if a password follows requirements
        :param password: str
        :return: bool
        """
        #TODO : This should also be handled by the front_end
        pass


    @staticmethod
    def is_email_valid(email):
        """
        Validate Email
        :param email: str
        :return: bool
        """
        user = User.objects.filter(email=email).first()
        if user is None:
            return True
        else:
            return False

    @staticmethod
    @require_http_methods(['POST'])
    def profile_settings(request):
        """
        Update User Profile
        :param request: HttpRequest
        :return: JsonResponse
        """

        status, msg = False, "Invalid Request"

        if request.user.is_authenticated:
            received_json_data = json.loads(request.body)

            user = request.user
            a = Account_DB.objects.filter(username=user.username).first()
            a.is_private = received_json_data.is_private
            a.save()
            # TODO: Add more settings most likely going to add a setting model
            status, msg = True, "Settings Updated Successfully"

        return JsonResponse({"status":status, "msg":msg})

