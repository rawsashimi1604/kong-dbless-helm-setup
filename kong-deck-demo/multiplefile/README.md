# commands

- merge multiple partial files: `deck file merge -o merged.yml exmaple.yml foo.yml`
- merge multiple complete config files with checks: `deck file render`

- validate files: `cat example.yml | deck file validate`

# problems

- merge dosent perform any checks on content (duplications, validations)
