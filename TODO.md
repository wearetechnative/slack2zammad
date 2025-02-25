# TODO/ROADMAP

## Next Version

- extra cli arguments:
 - --envfile
 - --version
 - --help
- nix package to run via Flake
- nix module to include with these options via Flake

```nix
services.slack2zammad = {
  enable = true
  envFile = /var/secrets/slack2zammad.env
}
```
- implementation howto for suitable for nix users
- new release using the [release runbook](RELEASE-RUNBOOK.md)

## Backlog

- seperate configuration file e.g. slack2zammad.config.yaml
  - group to create new tickets in
- refactoring of python codes with a module structure
- http mode
- More advanged ticket flows
  - which customer
  - priotity
- Add link to original message in slack channel in Zammad ticket.
- Full documentation
- PR in nixos/nixpkgs
- CONTRIBUTE.md
- Logo and header info about TechNative
- Create project logo
