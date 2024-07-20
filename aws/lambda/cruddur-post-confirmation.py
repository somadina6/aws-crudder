import json
import psycopg2
import  os

def lambda_handler(event,context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(event)
    print(context)
    
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        user_display_name       = user['name']
        user_handle             = user['preferred_username']
        user_email              = user['email']
        user_cognitio_id        = user['sub']

        params = [
            user_display_name,
            user_handle,
            user_cognitio_id,
            user_email,
    
        ]

        sql = '''
        INSERT INTO users 
        (display_name, handle, cognito_user_id, email) 
        VALUES(%s,%s,%s,%s)
        '''
        cur.execute(sql,tuple(params))
        conn.commit() 

    except (psycopg2.DatabaseError) as error:
        print('Error: ')
        print(error)
        
    finally:
        cur.close()
        conn.close()
        print('Database connection closed.')

    return event