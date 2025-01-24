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
            packages = let
              gcloud = google-cloud-sdk.withExtraComponents (with google-cloud-sdk.components; [
                gke-gcloud-auth-plugin
              ]);
            in [
              gcloud
              infisical
              kubectl
              mongosh
              poetry
              python310
              uv
            ];

            shellHook = ''
              VENV="./.venv/bin/activate"

              if [[ ! -f $VENV ]]; then
                ${poetry}/bin/poetry install --with dev --with ci
              fi

              source "$VENV"
            '';

            LD_LIBRARY_PATH = lib.makeLibraryPath [
              stdenv.cc.cc.lib
              stdenv.cc.cc
              zlib
            ];
          };
      }
    );
}
