# In2 Zammad

Slack App providing a Message Shortcut to create Zammad ticket from Slack
message

@luca read the rought [TODO](TODO.md)

## Install

### Prepare Slack

Create an app with this manifest...

```yaml
display_information:
  name: In2 Zammad
  description: Create tickets from messages
  background_color: "#ab6d22"
features:
  bot_user:
    display_name: Zammad
    always_online: false
  shortcuts:
    - name: Create ticket
      type: message
      callback_id: create_ticket
      description: Creates a ticket based on the message
oauth_config:
  scopes:
    bot:
      - commands
settings:
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```

Currently only the socket mode is working.

### Configure environment vars

Create a .env-file or set environment vars.

```bash
SLACK_APP_TOKEN=xoxb-XXXX....
SLACK_BOT_TOKEN=xapp-XXXX....
ZAMMAD_URL=https://my-zammad-domain.com
ZAMMAD_USER=zammad_user
ZAMMAD_PASSWD=zammad_password
```

### Without Nix

Install requirements with Pip of if you have a working nix with flake enabled.

### With Nix

nix develop

### Start application

python app.py

## CONTRIBUTE

### Issues, Bugs, and Feature Requests

File issue requests [in this repo](https://github.com/wearetechnative/slack2zammad/issues/new)

### Open Source & Contributing

Slack2zammad is open source and we appreciate contributions and positive feedback.

### Docs for Project Maintainers

Read the docs and roadmaps

- [Release runbook](RELEASE-RUNBOOK.md)
- [Roadmap](TODO.md)
- [Changelog](CHANGELOG.md)

## Credits

- [Zammad](https://zammad.com) - a great supportdesk system
- [zammadoo](https://github.com/flashdagger/zammadoo) - a fresh but nice working python client for Zammad

## License and Copyright

Copyright 2025 [TechNative B.V.](https://technative.eu) | Published under the [Apache License](LICENSE).
