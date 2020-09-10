from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from api.models import Likes as Like_DB

import json


class Likes:

    @staticmethod
    @require_http_methods(["POST"])
    def like_or_unlike(request):
        """
        User like a post or unlikes a post
        :param request: HttpResponse
        :return: JsonResoponse
        """
        status, msg = False, "Invalid Request"

        if request.user.is_authenticated:
            post_id = json.loads(request.body)["post_id"]
            type_of_post = json.loads(request.body)["type_of_post"].upper()

            l = Like_DB.objects.filter(
                username=request.user.username, post_id=post_id).first()

            if l:
                l.delete()
                status, msg = True, "Success"
            else:
                l = Like_DB(username=request.user.username, type_of_post=type_of_post, post_id=post_id)
                l.save()
                status, msg = True, "Success"

        return JsonResponse({"status":status, "msg":msg})


    @staticmethod
    @require_http_methods(["GET"])
    def get_likes(request):
        """
        Get Likes for a post
        Paginate list by 10
        :param request: HttpResponse
        :return: JsonResponse
        """
        status, theList, hasMore = False, [], False

        if request.user.is_authenticated:
            # type_of_post = json.loads(request.body)["type_of_post"].upper()
            post_id = json.loads(request.body)["post_id"]
            page_range = json.loads(request.body)["page_range"]

            l = Like_DB.objects.filter(post_id)
            p = Paginator(object_list=l, per_page=10)
            page = p.page(page_range)
            # TODO: theList representation should be an account object with only the need to know
            status, theList, hasMore = True, page.object_list, page.has_next()

        return JsonResponse({
            "status": status, "theList": theList, "hasMore": hasMore})




