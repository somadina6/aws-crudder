FROM python:3.10-slim-buster

# Inside Container
# Make a new folder inside the container
WORKDIR /backend-flask

# Outside container -> Inside container
# this contains library we want to install
COPY requirements.txt requirements.txt

# Install the python libraries
RUN pip3 install -r requirements.txt

COPY . .

# Set Env Vars
ENV FLASK_ENV=development
ENV PORT=4567

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
