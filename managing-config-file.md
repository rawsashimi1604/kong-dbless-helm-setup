# Managing declarative configuration

## Why manage declaration file

In the case of many services, managing everything in 1 file is unreliable and unsafe, multiple writes could occur at once time and could cause the file to be corrupted.

## Constraints

- Concurrency Control:
  - Ensure that write operations to the Kong configuration file are atomic, preventing partial updates that could lead to an inconsistent state.
  - Implement locking mechanisms to handle concurrent writes and reads, ensuring that only one process can perform write operations at a time, while still allowing multiple concurrent reads.
- Data Integrity:
  - Validation: Configuration file should be valid when loaded into kong
- Fault Tolerance:
  - File should be regularly backed up, or versioned, so rollback or restore from backup is possible.

## Method 1: Kong deck to compare file

![approach-1](./kong-deck-demo/kong-deploy.png)

## Method 2
