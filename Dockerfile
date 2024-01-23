FROM node:16.18

ENV PORT=3000

WORKDIR /root
COPY ./frontend-react-js ./frontend-react-js
RUN cd ./frontend-react-js   
RUN npm install
RUN cd ..



FROM python:3.10-slim-buster

# Inside Container
# Make a new folder inside the container


# Outside container -> Inside container
# this contains library we want to install
COPY ./backend-flask/requirements.txt ./backend-flask/requirements.txt

# Install the python libraries
RUN pip3 install -r ./backend-flask/requirements.txt

COPY ./backend-flask/ ./backend-flask/

# Set Env Vars
ENV FLASK_ENV=development

EXPOSE ${PORT}

CMD [ "npm", "start", ";", "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
