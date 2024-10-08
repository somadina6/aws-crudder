from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb
from lib.db import db

class MessageGroups:
   def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    sql = db.template('users','uuid_from_cognito_user_id')
    my_user_uuid = db.query_value(sql,{'cognito_user_id': cognito_user_id})

    print("UUID",my_user_uuid,flush=True)


    dynamodb_client = Ddb.client()

    data = Ddb.list_message_groups(dynamodb_client,my_user_uuid)
    print("list_message_groups:",data,flush=True)
    model['data'] = data
    return model