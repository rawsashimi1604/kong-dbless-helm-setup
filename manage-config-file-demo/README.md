# Config file management demo

This is a demo on managing config file of kong-dbless.

All related configuration is stored in this directory, and it is the source of truth for the kong deployment.

## Pull kong deck docker image

```shell
docker pull kong/deck:v1.36.1
```

## Merging files together

Use `deck file render`

```shell
kong file merge config1.yml config2.yml -o merged --format yaml
```

Script to run automatically:

```shell
sh merge_files.sh
```

## Validating the file

Use `deck file validate merged.yaml`

If empty, no errors, proceed.

## Run a kong image

```shell
docker run -d --name kong-dbless \
 -e "KONG_DATABASE=off" \
 -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
 -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
 -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
 -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
 -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" \
 -e "KONG_ADMIN_GUI_URL=http://localhost:8002" \
 -e KONG_LICENSE_DATA \
 -p 8000:8000 \
 -p 8443:8443 \
 -p 8001:8001 \
 -p 8444:8444 \
 -p 8002:8002 \
 -p 8445:8445 \
 -p 8003:8003 \
 -p 8004:8004 \
 kong/kong-gateway:2.8.4.7-alpine
```

## Load the configuration

```shell
curl -i -X POST http://localhost:8001/config \
  --form config=@merged.yaml
```

## Do a helm deploy
