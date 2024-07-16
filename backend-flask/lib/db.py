from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app

class Db:
    def __init__(self):
        self.init_pool()
    
    def template(self,*args):
        pass
    
    def print_sql(self,sql,title='LOGGER PRINT'):
        cyan ='\033[96m'
        no_color = '\033[0m'
        print(f"{cyan}PRINT----{title}----{no_color}",flush=True)
        print(sql, '\n',flush=True)

    def init_pool(self):
        connection_url = os.getenv("CONNECTION_URL")
        self.pool = ConnectionPool(connection_url) 

    def query_commit(self, sql, params={}):  
        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern=pattern,string=sql)
        self.print_sql(sql,'SQL')
 
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    if is_returning_id:
                        returning_id = cur.fetchone()[0]
                        # conn.commit()
                        self.print_sql(title='returning_id',sql=returning_id)
                    
                    else:
                         cur.fetchone()[0]
        
        
        except Exception as err:
            # self.print_sql_err(err)
            self.print_sql(err,title='Error query commit:')

        return returning_id

    def query_array_json(self,sql_input,params={}):
        sql = self.query_wrap_array(sql_input)
        self.print_sql(sql)
        self.print_sql(params)
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

    def print_sql_err(self,err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno

        # print the connect() error
        print ("\npsycopg ERROR:", err, "on line number:", line_num)
        print ("psycopg traceback:", traceback, "-- type:", err_type)

        # print the pgcode and pgerror exceptions
        if err.pgerror:
             print ("pgerror:", err.pgerror)
        if err.pgcode:
            print ("pgcode:", err.pgcode, "\n")

db = Db()