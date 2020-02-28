import hmac
from hashlib import sha1

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_POST
from rest_framework.views import APIView

from django.shortcuts import render

class Frontend(APIView):
    def get(self, request):
        return render(request, "build/index.html")