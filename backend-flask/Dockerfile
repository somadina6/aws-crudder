# Builds the initial layer
FROM python:3.10-slim-buster

# Working Directory in Container
WORKDIR /backend-flask

# Copy the requirements out to in
COPY requirements.txt requirements.txt

# install dependencies from requitrements
RUN pip3 install -r requirements.txt


COPY . .

#Set Environment variable
ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
