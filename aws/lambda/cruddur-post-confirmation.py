import json
import psycopg2
import  os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)
    
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        user_display_name       = user['name']
        user_handle             = user['preferred_username']
        user_email              = user['email']
        user_cognitio_id        = user['sub']

        sql = f'''
        INSERT INTO users 
        (display_name, handle, cognito_user_id, email) 
        VALUES('{user_display_name}', '{user_email}', '{user_cognitio_id}','{user_email})
        '''
        cur.execute(sql)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event