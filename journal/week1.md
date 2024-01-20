# 1 — App Containerization

## Created a Dockerfile
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
```
