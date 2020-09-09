from api.models import Follows as Follows_DB


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
    @require_http_method(["POST"])
    def follow_or_unfollow(request):
        """
        Follow or unfollow  a user
        @param:request HttpRequest 
        @return: JsonResponse
        """
        if request.user.is_authenticated:
            user = request.user
            F
            
