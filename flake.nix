{
  description = "Dev environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    utils,
    nixpkgs,
    ...
  }:
    utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in {
        devShells.default = with pkgs;
          mkShell {
            packages = [
              infisical
              python310
              poetry
            ];

            shellHook = ''
              VENV="./.venv/bin/activate"

              if [[ ! -f $VENV ]]; then
                ${poetry}/bin/poetry install --with dev --with ci
              fi

              source "$VENV"
            '';

            LD_LIBRARY_PATH = lib.makeLibraryPath [stdenv.cc.cc];
          };
      }
    );
}
