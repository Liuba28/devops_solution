![Logo of the project](/home/gis2/Desktop/fatmap.png)

# Devops solution

The following sections show the solution for the Devops/GIS Engineer technical task.

## Create GBDX server component

Clone the repo and enter the directory of the project from the terminal.
geoserver.py is the GBDX server component.

## Dockerise the component

Expose the service by running in the terminal:

```shell
docker-compose up
```
Using REST client of choice, send request to machine running service to port 3004 with GeoJSON as payload.

## Deploy the component to a local Kubernetes cluster

Go to the kubernetes directory and create a Deployment:

```shell
kubectl create -f ./deployment.yaml
```

View the Pod:

```shell
kubectl get pods
```

Create a Service:

```shell
kubectl create -f ./service.yaml
```

Access service:

```shell
minikube service minikube2
```

This will automatically opens up a browser window and shows the "Welcome! You have reached the Fatmap API GBDX Server Component." message.

To be able to POST and recieve GeoJSON from the local machine use REST client and local IP address. 




