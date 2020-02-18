from django.shortcuts import render
from django.http import JsonResponse
<<<<<<< HEAD


# Create your views here.
=======
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
>>>>>>> 1e258a215a3820cf58befb652e9b837768f426b8
def userByUsername(request, username):
  if request.method == "POST":
    print(username) 

  return JsonResponse({'username':username})
