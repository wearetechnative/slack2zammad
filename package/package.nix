{ lib
, python3Packages
, python
, ...
 }:

python3Packages.buildPythonApplication rec {
  pname = "slack2zammad";
  version = "0.2.0";

  src = ./..;

  dependencies = [(python.withPackages (ps: with ps; [
    slack-bolt
    zammadoo
    python-dotenv
  ]))];

  meta = {
    homepage = "https://github.com/wearetechnative/slack2zammad";
    license = lib.licenses.asl20;
    maintainers = with lib.maintainers; [ Caspersonn ];
  };
}
