from flask import Flask
from flask import request,abort,jsonify
from flask_cors import CORS, cross_origin
import os

from lib.cognito_jwt_token import CognitoJwtToken,TokenVerifyError

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *

# HoneyComb ------------------------------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


# X-Ray
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Rollbar 
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)



# Initialize tracing and an exporter that can send data to Honeycomb
# provider = TracerProvider()
# processor = BatchSpanProcessor(OTLPSpanExporter())
# provider.add_span_processor(processor)

# Show the logs within backend
# processor2 = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(processor2)

app = Flask(__name__)

XRayMiddleware(app, xray_recorder)

cognito_token_veri = CognitoJwtToken(
  user_pool_id=os.getenv('AWS_COGNITO_USER_POOL_ID'),
  region=os.getenv('AWS_DEFAULT_REGION'),
  user_pool_client_id=os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID'))


# Rollbar Init
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')


with app.app_context():
    """init rollbar module"""
    
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
print(frontend) #print
origins = [frontend, backend]


CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)


@app.route('/rollbar/test')
def rollbar_test():
    print('SOMA',rollbar_access_token)
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"


@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  access_token = CognitoJwtToken.extract_access_token(request.headers)

  try:
    claims = cognito_token_veri.verify(access_token)
    app.logger.debug('authenticated')
    app.logger.debug(claims)
    cognito_user_id = claims['sub']

    model = MessageGroups.run(cognito_user_id=cognito_user_id)
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
      
  except TokenVerifyError as e:
    _ = request.data
    app.logger.info(e)
    return {}, 401

  

@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
def data_messages(message_group_uuid):
  

  try:
    access_token = CognitoJwtToken.extract_access_token(request.headers)
    
    claims = cognito_token_veri.verify(access_token)
    app.logger.debug('authenticated')
    cognito_user_id = claims['sub']

    model = Messages.run(
      message_group_uuid=message_group_uuid,
      cognito_user_id=cognito_user_id
      )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
      
  except TokenVerifyError as e:
    _ = request.data
    app.logger.info(e)
    return {}, 401
  

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  # extract user details from request body
  user_receiver_handle = request.json.get('handle', None)
  message_group_uuid = request.json.get('message_group_uuid',None)
  message = request.json['message']

  try:
    # extract token from request header and verify 
    access_token = CognitoJwtToken.extract_access_token(request.headers)
    claims = cognito_token_veri.verify(access_token)
    cognito_user_id = claims['sub']

    # initialize create message method
    if message_group_uuid == None:
      # Create for the first time
      model = CreateMessage.run(
        mode="create",
        message=message,
        cognito_user_id=cognito_user_id,
        user_receiver_handle=user_receiver_handle
      )
    else:
      # Push onto existing Message Group
      model = CreateMessage.run(
        mode="update",
        message=message,
        message_group_uuid=message_group_uuid,
        cognito_user_id=cognito_user_id
      )

    if model['errors'] is not None:
      return model['errors'], 422
    elif model['data'] is not None:
      return model['data'], 200
    else:
      return {}, 201

  except TokenVerifyError as e:
    _ = request.data
    app.logger.info(e)
    return {}, 401
    
  

# Home Activities Endpoint
@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture('activities_home')
def data_home():
  access_token = CognitoJwtToken.extract_access_token(request.headers)

  try:
    claims = cognito_token_veri.verify(access_token)
    app.logger.info('claims')
    app.logger.info(claims)
    app.logger.info(claims['username'])
  except TokenVerifyError as e:
    _ = request.data
    app.logger.info(e)
    # abort(403)


  data = HomeActivities.run(claims['username'])
  # app.logger.info(data)
  return data, 200

# Notifications
@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  

@app.route("/api/activities", methods=['POST'])
@cross_origin()
def data_activities():
  access_token = CognitoJwtToken.extract_access_token(request.headers)

  try:
    claims = cognito_token_veri.verify(access_token)
    app.logger.info('claims')
    app.logger.info(claims)
    user_handle = claims['username']
  except TokenVerifyError as e:
    _ = request.data
    app.logger.info(e)

  message = request.json['message']
  user_handle = 'somadina600'

  ttl = request.json['ttl']
  create_activity = CreateActivity()
  
  model = create_activity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivities.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/users/@<string:handle>/short", methods=['GET'])
def data_users_short(handle):
  data = UsersShort.run(handle)
  return data, 200

if __name__ == "__main__":
  app.run(debug=True)