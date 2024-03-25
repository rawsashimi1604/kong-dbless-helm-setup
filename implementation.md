# implementation

- CI level
- use kong deck to merge, validate,
- merge first then validate if fail CI fail
- first merge is to test
- run kong container to double check config can be pushed

- 1 Kong 1 Repo with all configs in the same repo
- CI level

  - Run kong deck docker image
  - do a merge
  - do a validate
  - start a kong docker dbless image
  - try to post the config
  - if 200 PASS

- CD level
  - Do a helm deploy
    - init container
      - kong deck merge
      - rolling update
