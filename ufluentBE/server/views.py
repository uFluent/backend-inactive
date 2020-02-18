from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def userByUsername(request, username):
  if request.method == "POST":
    print(username) 

  return JsonResponse({'username':username})
