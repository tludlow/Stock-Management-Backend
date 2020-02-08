import hmac
from hashlib import sha1

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_POST

import os

# src: https://simpleisbetterthancomplex.com/tutorial/2016/10/31/how-to-handle-github-webhooks-using-django.html
@require_POST
@csrf_exempt
def deploy(request):
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature != settings.GITHUB_WEBHOOK_KEY:
        return HttpResponseForbidden((header_signature, " OTHER ", settings.GITHUB_WEBHOOK_KEY))

    os.system("cd ~/apache/htdocs/backend/ && git pull")
    os.system("/usr/sbin/httpd -d $HOME/apache -k restart")

    # If request reached this point we are in a good shape
    return HttpResponse('success')
