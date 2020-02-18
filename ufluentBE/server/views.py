from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from pypika import Query,Table
import re

# Create your views here.

def selectUserByUsername(request,username):
  try:
    connection = psycopg2.connect(user='tom',password='password',database='ufluent')
    cursor = connection.cursor()
    users = Table('schema_users')
    selectUser = Query.from_(users).select('avatarUrl', 'language', 'score', 'img_id').where(users.username == username)
    cursor.execute(str(selectUser))
    print('fetching user data...')
    userData = cursor.fetchone()
    if not userData:
      error = {'msg': 'User does not exist', 'status':404 }
      return JsonResponse(error, status=404)
    else:
      return JsonResponse({'user': {'avatarUrl': userData[0],
                                  'language' : userData[1],
                                  'score' : userData[2],
                                  'img_id': userData[3]}})
      
  except (Exception, psycopg2.Error) as error:
    if hasattr(error,'pgerror'):
      print('Error occured ---->',error.pgerror)
      errorLines = re.findall(r"[^\n]+\n",error.pgerror)
      return JsonResponse({'error': {'code':error.pgcode,
                                     'msg':errorLines[0][:-1]}})
    else:
      return JsonResponse({'error': 'some error'})
    
  finally:
    if(connection):
      cursor.close()
      connection.close()
      print('db connection closed.')


def patchUserByUsername(request, username):
  try:
    



@csrf_exempt
def userByUsername(request, username):
  if (request.method == "GET"):
    return selectUserByUsername(request,username)
  if (request.method == "PATCH"):
    return 