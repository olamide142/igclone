from api.models import Image
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from api.forms import ImageUploadForm
from api.services.tools import Tools
from api.models import Image as Image_DB
from api.models import Comment as Comment_DB

import json

class Image:

    @staticmethod
    @require_http_methods(["POST"])
    def image_upload(request):
        pass
        """
        Upload an image
        :param request: HttpRequest
        :return: JsonResponse
        """
        status, msg = False, "Invalid Request"

        form = ImageUploadForm(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            t = Tools.handle_uploaded_file(request.FILES['file'], form.extension)
            if t[0]:
                #delete profile pic if it exist
                if form.category == "PI":
                    pi = Image_DB.objects.filter(username=form.username, category=form.category)
                i = Image_DB(username=form.username, category=form.category, url=t[1])
                if Image.delete_image(pi.url, request, form.category):
                    i.save()
                    status, msg = True, "Success"

        return JsonResponse({"status":status, "msg":msg})


    @staticmethod
    @require_http_methods(["POST"])
    def delete_image(request, cat=None, image_url=None):
        pass
        if request.user.is_authenticated:

            if cat == "PI":
                return Tools.delete_image(image_url)
            # delete an regular image post
            image_url = json.loads(request.body)["image_url"]
            Tools.delete_image(image_url)

            # TODO: delete comments and likes associated with this image
