from api.models import Follows as Follows_DB
from api.models import Account as Account_DB
from django.views.decorators.http import require_http_methods
from django.http import  JsonResponse, HttpResponse

import json


class Follows:

    
    @staticmethod
    def each_other_status(username1, username2):
        """
        Check the following stats between 2 users
        :param username1: User.username
        :param username2: User.username
        :return: dict() # {'olamide': 1, 'victor': 0} Olamide follows Victor
        """
        # probably not the best query
        f = Follows_DB.objects.filter(username1=username1, username2=username2).first() \
            or Follows_DB.objects.filter(username1=username2, username2=username1).first()

        if f is None:
            return {username1+"follows" : "0", username2+"follows" : "0",
                    username1 + "blocked": "0", username2 + "blocked": "0",
                    username1 + "muted": "0", username2 + "muted": "0"}
        else:
            a,b = f.is_following.split("-")
            c,d = f.is_blocked.split("-")
            e,f = f.is_muted.split("-")
            return {f.username1 + "follows": a, f.username2 + "follows": b,
                    f.username1 + "blocked": c, f.username2 + "blocked": d,
                    f.username1 + "muted": e, f.username2 + "muted": f}


    @staticmethod
    def get_follows_count(username):
        """
        Get the total Number of followers and
        account this user is following
        :param username: User.username
        :return: dict({'followers':100, 'following':90})
        """
        follows = {"followers":0, "following":0}

        # f1 [following-followers]
        f1 = Follows_DB.objects.filter(username1=username)
        # f2 [followers-following]
        f2 = Follows_DB.objects.filter(username2=username)

        for i in f1:
            x, y = i.is_following.split("-")
            follows["following"] += int(x)
            follows["followers"] += int(y)

        for i in f2:
            x, y = i.is_following.split("-")
            follows["following"] += int(y)
            follows["followers"] += int(x)

        return follows


    @staticmethod
    @require_http_methods(["POST"])
    def follow_or_unfollow(request):
        """
        Follow or unfollow  a user
        @param:request HttpRequest 
        @return: JsonResponse
        """
        if request.user.is_authenticated:
            user = request.user
            username_to_follow = \
                Account_DB.objects.filter(username=json.loads(request.body)['username']).first()

            if username_to_follow.is_private:
                pass # Send a follow request to user first
                return JsonResponse({'status': True, 'msg': 'Success'})

            f = Follows_DB.objects.filter(username1=user.username, username2=username_to_follow).first() \
                or Follows_DB.objects.filter(username1=username_to_follow, username2=user.username).first()

            if f is not None:
                if f.username1 == user.username:
                    x,y = f.is_following.split("-")
                    x = abs(int(x) + -1) # Invert the Val from 0-1, vice versa
                elif f.username2 == user.username:
                    x, y = f.is_following.split("-")
                    y = abs(int(y) + -1) # Invert the Val from 0-1, vice versa
                f.is_following = f"{x}-{y}"
                f.save()
            else:
                f = Follows_DB(username1=user.username, username2=username_to_follow, is_following="1-0")
                f.save()
        return JsonResponse({ 'status' : True, 'msg' : 'Success'})


    @staticmethod
    def request_to_follow(user_logged_in, user_to_follow):
        pass
