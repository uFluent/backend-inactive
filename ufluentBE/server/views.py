from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def userByUsername(request, username):
  if request.method == "POST":
    print(username) 

  return JsonResponse({'username':username})
