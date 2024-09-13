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
              (poetry.override {python3 = python310;})
            ];

            shellHook = ''
              source ./.venv/bin/activate
            '';

            LD_LIBRARY_PATH = lib.makeLibraryPath [
              stdenv.cc.cc
            ];
          };
      }
    );
}
