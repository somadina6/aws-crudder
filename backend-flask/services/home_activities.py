from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import db

tracer = trace.get_tracer('home.activities')

class HomeActivities:
  def run(self):
    sql = db.template('activities','home')
    results = db.query_array_json(sql)
    return results