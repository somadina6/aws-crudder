import uuid
from datetime import datetime, timedelta, timezone
from lib.db import db

class CreateActivity:
  def validations():
    pass

  def run(self,message, user_handle, ttl):
    model = {
      'errors': None,
      'data': None
    }
    user_uuid = ''
    

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      expires_at = (now + ttl_offset)
      uuid_returned = self.create_activity(user_handle,message,expires_at)
      model['data'] = self.query_object_activity(uuid_returned)
    return model



  def create_activity(self,handle,message,expires_at):

    sql = f'''
      INSERT INTO public.activities (user_uuid, message, expires_at)
      VALUES(
      (SELECT uuid FROM public.users WHERE users.handle = %(handle)s LIMIT 1),
      %(message)s, 
      %(expires_at)s)
      RETURNING uuid;
    '''

    uuid = db.query_commit(sql, 
    {"handle":handle, 
    "message":message,
    "expires_at":expires_at})

    return uuid


  def query_object_activity(self,uuid_returned):
    sql =  f'''
    SELECT 
      a.uuid,
      u.display_name,
      u.handle,
      a.message,
      a.created_at,
      a.expires_at 
    FROM public.activities as a
    INNER JOIN public.users as u ON a.user_uuid = u.uuid
    WHERE a.uuid = %(uuid_returned)s
    '''

    result = db.query_object_json(sql,{'uuid_returned':uuid_returned})
    return result
    

    
  