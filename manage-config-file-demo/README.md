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
kong file render config1.yml config2.yml -o merged --format yaml
```

Script to run automatically:

```shell
sh merge_files.sh
```

## Validating the file

Use `deck file validate merged.yaml`

If empty, no errors, proceed.
