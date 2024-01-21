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


## Pushing & Tagging An Image To DockerHub
* Created a public repo on DockerHub
* Login to Docker via CLI:
```
docker login --username=somadina6
```

* Tag the local image with repo:tagname:
```
docker tag local-mage:tagname repo:tagname
docker tag aws-crudder-backend-flask:latest somadina6/crudder-aws:backend-flask
docker tag aws-crudder-frontend-react-js:latest somadina6/crudder-aws:frontend-react
```

* Push the images to the DockerHub repo:
```
docker push somadina6/crudder-aws:backend-flask 
docker push somadina6/crudder-aws:frontend-react 
```

