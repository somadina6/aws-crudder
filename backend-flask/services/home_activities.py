from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import pool, query_wrap_array,query_wrap_object

tracer = trace.get_tracer('home.activities')

class HomeActivities:
  def run(username=None):
    sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
    print(sql)

    print("-------------------------SQL----------------------------",flush=True)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchone()
        print(rows[0],flush=True)
        results = rows

    return results[0]