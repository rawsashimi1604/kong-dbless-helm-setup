# Managing declarative configuration

## Why manage declaration file

Kong Dbless only allows all configuration to be stored into 1 config file. In the case of large scale or multiple teams managing api configurations, managing everything in 1 file is unreliable and unsafe, multiple writes could occur at once time and could cause the file to be corrupted.

## Constraints

- Concurrency Control:
  - Ensure that write operations to the Kong configuration file are atomic, preventing partial updates that could lead to an inconsistent state.
  - Implement locking mechanisms to handle concurrent writes and reads, ensuring that only one process can perform write operations at a time, while still allowing multiple concurrent reads.
- Data Integrity:
  - Validation: Configuration file should be valid when loaded into kong
  - Single source of truth for configuration file.
- Fault Tolerance:
  - File should be regularly backed up, or versioned, so rollback or restore from backup is possible.

## Method 1: Kong deck (ApiOps tool) to compare file to test kong container, then dump config file, and upload to kong pods

![approach-1](./kong-deck-demo/kong-deploy.png)

- Use `kong deck` as a cli tool to help manage configuration. [Click here to find out more about deck.](https://docs.konghq.com/deck/latest/)
- [Video](https://www.youtube.com/watch?v=fzpNC5vWE3g&ab_channel=Kong)
- It is not fully compatible with kong dbless (not able to sync), but there is a workaround we can do.
- Also provides drift detection, can help sync instance with the input configuration file. (synchronization)
- Also feature with open api spec to kong specification, able to help with APIOps

- Essential commands:
  - `deck file validate` - validate the deck configuration state file.
  - `deck gateway diff` - check the diff with existing kong instance.
  - `deck gateway sync` - sync the diff with existing kong instance.
  - `deck gateway dump` - dump existing kong configuration to file. (generate new config)

## Method 2: Kong deck (ApiOps tool) simpler approach, use render

- Using kong deck, we can manage seperate complete configurations in different files or repos
- Merge them together using `kong file render config1.yml config2.yml -o merged --format json`
- This would generate the config file need to start the new kong instance.

## Method 3: Gitops in-house tool approach

Link to medium article: <https://surenraju.medium.com/gitop-approch-to-configuration-management-in-kong-dbless-mode-bf0f9fc0a68e>

- Provide some sort of json schema to validate the configuration (validate at both merged, and individual configuration files)

- For synchronization, use a sidecar container or cron job every x seconds to send http request to `/GET config`, if different from our main config (which can be pulled from Git repo), we can generate an alert whilst `/POST config` to sync.

- Split declaration into multiple files
- `global` file, globally declared plugins:

```yaml
plugins:
 - name: jwt
   config:
     header_names: "my-header"
```

- `service` file, per-service API route configuration defined in a seperate yaml file.

```yaml
- name: my-route
   paths:
   - /my-route
   methods:
   - GET
   plugins:
   - name: cors
     config:
       origins:
       - example.com
```

- `master` file, merged configuration

```yaml
services:
 - name: my-service
   url: https://example.com
   routes:
     - name: my-route
     paths:
     - /my-route
     methods:
     - GET
 plugins:
 - name: jwt
   config:
     header_names: "my-header"
 - name: cors
   config:
     origins:
     - example.com
```

- When file merged, push the changes to a tmp branch, we can run some sort of integration testing to a mock kong pod, to run the config command
- If it works we can merge into main branch, which will then trigger a helm rolling upgrade to all upstream kong pods to reload and receive new configuration
