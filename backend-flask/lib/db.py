from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app

class Db:
    def __init__(self):
        self.init_pool()
    
    def template(self,*args):
        pathing = list((app.root_path,'db','sql',) + args)
        pathing[-1] = pathing[-1] + ".sql"

        template_path = os.path.join(*pathing)

        green = '\033[92m'
        no_color = '\033[0m'
        print("\n")
        print(f'{green} Load SQL Template: {template_path} {no_color}')

        with open(template_path, 'r') as f:
            template_content = f.read()
        return template_content

    def print_sql(self,sql,title='LOGGER PRINT'):
        cyan ='\033[96m'
        no_color = '\033[0m'
        print(f"{cyan}PRINT----{title}----{no_color}",flush=True)
        print(sql, '\n',flush=True)

    def init_pool(self):
        connection_url = os.getenv("CONNECTION_URL")
        self.pool = ConnectionPool(connection_url) 

    def query_commit(self,sql,params={},verbose=True):
        if verbose:
            self.print_sql(title='commit with returning',sql=sql)

        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql)

        try:
            with self.pool.connection() as conn:
                cur =  conn.cursor()
                cur.execute(sql,params)
                if is_returning_id:
                    returning_id = cur.fetchone()[0]
                conn.commit() 
                if is_returning_id:
                    return returning_id
        except Exception as err:
            print(err)

    def query_array_json(self,sql_input,params={}):
        sql = self.query_wrap_array(sql_input)
      
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,params)
                json = cur.fetchone()  
                if json is None:
                    self.print_sql('JSON is None','Error')  
        return json[0]

    def query_object_json(self,sql_input,params={}):
        sql = self.query_wrap_object(sql_input)
        self.print_sql(sql)
        self.print_sql(params)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,params)
                json = cur.fetchone()
                if json is None:
                    self.print_sql('JSON is None','Error')
                else:
                    self.print_sql(json[0],'JSON RETUNED') 

        return json[0]

    def query_wrap_object(self,template):
        sql = f"""
        (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
        {template}
        ) object_row);
        """
        return sql

    def query_wrap_array(self,template):
        sql = f"""
        (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
        {template}
        ) array_row);
        """
        return sql


db = Db()