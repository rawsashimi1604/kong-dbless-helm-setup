# Kong dbless setup

## Create mock deployment and service

```bash
cd mock
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

## Create a config map from kong config file

```bash
kubectl create configmap kong-config --from-file=kong.yml --dry-run=client -o yaml | kubectl apply -f -
```

## Install kong dbless

```bash
helm repo add kong https://charts.konghq.com
helm repo update
helm install kong-dbless kong/kong --values=values.yaml
```

## Getting URL for service

```bash
minikube service <service_name> --url
```
