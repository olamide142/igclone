from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.paginator import Paginator

from api.models import Comment as Comment_DB
from api.models import Image as Image_DB

import json
class Comment:

    @staticmethod
    @require_http_methods(["POST"])
    def add_comment(request):
        """
        Add a comment
        :param request: HttpResponse
        :return: JsonResponse
        """
        status, msg = False, "Invalid Request"

        if request.user.is_authenticated:
            comment = json.loads(request.body)['comment']
            type_of_post = json.loads(request.body)['type_of_post'].upper()
            post_id = json.loads(request.body)['post_id']
            # check type_of_post is valid
            check = False
            if type_of_post == "IM":
                i = Image_DB.objects.filter(image_id=post_id).first()
                if i:
                    check = True
            elif type_of_post == "CM":
                c = Comment_DB.objects.filter(comment_id=post_id).first()
                if c:
                    check = True
            if check:
                c = Comment_DB(
                    username=request.user.username,
                    type_of_post=type_of_post,
                    post_id=post_id, content=comment)
                c.save()
                status, msg = True, "Success"

        return JsonResponse({"status":status, "msg":msg})


    @staticmethod
    @require_http_methods(["GET"])
    def fetch_comments(request):
        """
        Fetch comments made under a post
        Paginate by 10 comments per respnse
        :param request: HttpResponse
        :return: JsonResponse
        """
        status, theList, hasMore = False, [], False

        if request.user.is_authenticated:
            post_id = json.loads(request.body)["post_id"]
            page_range = json.loads(request.body)["page_no"] or 1

            c = Comment_DB.objects.filter(post_id=post_id)
            p = Paginator(object_list=c, per_page=10)
            page = p.page(page_range)
            status, theList, hasMore = True, page.object_list, page.has_next()
        return JsonResponse({
            "status":status, "theList":theList, "hasMore":hasMore})



    @staticmethod
    @require_http_methods(["DELETE"])
    def delete_comment(request):
        """
        Delete user's comment
        :param request: HttpRequest
        :return: JsonResponse
        """
        status, msg = False, "Invalid Request"
        comment = Comment_DB.objects.filter(
            comment_id = json.loads(request.body)["comment_id"]).first()

        if request.user.is_authenticated and (comment is not None):
            if comment.username == request.user.username:
                comment.delete()
                status, msg = True, "Success"

        return JsonResponse({"status":status, "msg":msg})




    @staticmethod
    @require_http_methods(["GET"])
    def get_total_comment(request):
        """
        Get the total number of comments
        under a post
        :param request: HttpResponse
        :return: JsonResponse
        """
        status, num = False, 0

        if request.user.is_authenticated:
            post_id = json.loads(request.body)["post_id"]
            c = Comment_DB.objects.filter(post_id=post_id)
            status, num = True, len(c)

        return JsonResponse({"status":status, "num":num})
