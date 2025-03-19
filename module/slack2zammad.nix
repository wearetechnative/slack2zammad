{
  config,
  pkgs,
  lib,
  ...
}:
let
  cfg = config.services.slack2zammad;
  defaultUser = "slack2zammad";
  defaultGroup = defaultUser;
  defaultSpaceDir = "/var/lib/slack2zammad";
in
{
  options = {
    services.slack2zammad = {
      enable = lib.mkEnableOption "";

      user = lib.mkOption {
        type = lib.types.str;
        default = defaultUser;
        example = "yourUser";
        description = ''
          The user to run Slack2zammad as.
          By default, a user named `${defaultUser}` will be created.
        '';
      };

      group = lib.mkOption {
        type = lib.types.str;
        default = defaultGroup;
        example = "yourGroup";
        description = ''
          The group to run Slack2zammad under.
          By default, a group named `${defaultGroup}` will be created.
        '';
      };

      envFile = lib.mkOption {
        type = lib.types.nullOr lib.types.path;
        default = "/etc/slack2zammad.env";
        example = "/etc/slack2zammad.env";
        description = ''
          File containing extra environment variables. For example:

          ```
          SLACK_APP_TOKEN=xoxb-000000000000000000000000000000000000000000000000000
          SLACK_BOT_TOKEN=xapp-00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
          ZAMMAD_URL=https://eeeeeeeeeeeeeeeeeeeeeeeeeeeee
          ZAMMAD_USER=xxxx@yyyyy.zz
          ZAMMAD_PASSWD=00000000000000000000
          ```
        '';
      };
    };
  };

  config = lib.mkIf cfg.enable {
    systemd.services.slack2zammad = {
      description = "Slack2zammad service";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];

      #preStart = lib.mkIf (!lib.hasPrefix "/var/lib/" cfg.spaceDir) "mkdir -p '${cfg.spaceDir}'";
      serviceConfig = {
        Type = "simple";
        User = "${cfg.user}";
        Group = "${cfg.group}";
        EnvironmentFile = lib.mkIf (cfg.envFile != null) "${cfg.envFile}";
        ExecStart =
          "${config.system.path}/bin/slack2zammad";
        Restart = "on-failure";
      };
    };

    users.users.${defaultUser} = lib.mkIf (cfg.user == defaultUser) {
      isSystemUser = true;
      group = cfg.group;
      description = "Slack2zammad daemon user";
    };

    users.groups.${defaultGroup} = lib.mkIf (cfg.group == defaultGroup) { };
  };

  meta = {
    maintainers = with lib.maintainers; [ Caspersonn ];
  };
}
