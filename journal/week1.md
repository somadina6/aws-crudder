# 1 — App Containerization

## Created a Dockerfile - Backend
* I created a Python image layer
* To install flask requirements during image building
* Runs flask in the container on the run command

## Key Takeaways
* Debugging process of setting up Environment Variables
* Familiar with tags such as '-i', '-d' and '-t' in docker build & docker run

### Code  
```
# building the image
docker build -t tagname </DockerfileDirectory>
```

```
# run a container of the image
docker run -it <imagename>
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```


## Created Dockerfile - FrontEnd

