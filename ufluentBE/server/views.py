from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from pypika import Query, Table
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def userByUsername(request, username):
    if request.method == "POST":
        print(username)

    return JsonResponse({'username': username})


@csrf_exempt
def postByUsername(request):
    jsonRequestData = json.loads(request.body)
    if request.method == 'POST':
        try:

            connection = psycopg2.connect(
                user='mustafa', password='password123', database='ufluent_test')
            cursor = connection.cursor()
            users = Table('schema_users')
            postUser = Query.into(users).columns('username', 'language').insert(jsonRequestData['username'], jsonRequestData['language']
                                                                                )
            try:
                cursor.execute(str(postUser))
                print(str(postUser))
            except(Exception, psycopg2.IntegrityError)as error:
                cursor.execute("ROLLBACK;")
                print(error)
            else:
                cursor.execute("COMMIT;")
                print(request.body)
                # userData = cursor.execute(str(postUser))
            return JsonResponse({'user': 1})
        except (Exception, psycopg2.Error) as error:
            print('Error occured ---->', error)
            # return JsonResponse({'error':error})
            return HttpResponse("<html><body>Error $s</body></html>")
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('db connection closed.')
