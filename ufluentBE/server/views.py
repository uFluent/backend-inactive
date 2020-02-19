from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from pypika import Query,Table,Field
from pypika.enums import Arithmetic
import re, json

# Create your views here.

def selectUserByUsername(request,username):
  try:
    connection = psycopg2.connect(user='tom',password='password',database='ufluent_test')
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
  requestData = json.loads(request.body)
  try:
    connection = psycopg2.connect(user='tom',password='password',database='ufluent_test')
    cursor = connection.cursor()
    users = Table('schema_users')
    textColumnsToChange = []
    intColumnsToChange = []    
    textColumnsToChange.append('avatarUrl') if 'avatarUrl' in requestData else '' 
    textColumnsToChange.append('language') if 'language' in requestData else ''     
    intColumnsToChange.append('score') if 'score' in requestData else ''     
    intColumnsToChange.append('img_id')if 'img_id' in requestData else ''
    
    if not len(intColumnsToChange) == 0 and not len(textColumnsToChange) == 0:
      return JsonResponse({'msg':'Can only patch (avatarUrl and language) or (img_id and score) at the same time.'},status=400)
    
    try:
      if len(textColumnsToChange) == 2:
        patchUser = Query.update(users).set(textColumnsToChange[0], requestData[textColumnsToChange[0]]).set(textColumnsToChange[1], requestData[textColumnsToChange[1]]).where(users.username == username)
        print(str(patchUser))
        patchUser = str(patchUser)
        cursor.execute(patchUser)
      elif len(textColumnsToChange) == 1:
        patchUser = Query.update(users).set(textColumnsToChange[0], requestData[textColumnsToChange[0]]).where(users.username == username)
        patchUser = str(patchUser)
        cursor.execute(patchUser)
        
      if len(intColumnsToChange) == 2:
        patchUser = """UPDATE schema_users SET score = score + %s, img_id = img_id + %s WHERE schema_users.username=%s;""",(requestData['score'],requestData['img_id'],username)
        cursor.execute(*patchUser)
      elif len(intColumnsToChange) == 1:
        patchUser = """UPDATE schema_users SET {0} = {1} + %s WHERE schema_users.username=%s;""".format(intColumnsToChange[0],intColumnsToChange[0]),(requestData[intColumnsToChange[0]],username)
        cursor.execute(*patchUser)
      else:
        return JsonResponse({'msg':'No valid patch data in request'},status=400)
      
    except Exception as error:
      cursor.execute('ROLLBACK;')
      print('**************************', error)
      return JsonResponse({'msg':'Error patching data'},status=500)
    else:
      cursor.execute('COMMIT;')
      print('success')
      return selectUserByUsername(request,username)
    
  except (Exception, psycopg2.Error) as error:
    print(error, '<<<<<<<<<<<<<<<<<<<<<<<')
    return JsonResponse({'msg':'error has occured'}, status=500)
  
  finally:
    if(connection):
      cursor.close()
      connection.close()
      print('db connection closed.')



@csrf_exempt
def userByUsername(request, username):
  if (request.method == "GET"):
    return selectUserByUsername(request,username)
  if (request.method == "PATCH"):
    return patchUserByUsername(request,username)