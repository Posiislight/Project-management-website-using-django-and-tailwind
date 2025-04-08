{ pkgs }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.mysqlclient
    pkgs.python312Packages.mysqlclient
    pkgs.mysql
    pkgs.libmysqlclient
    pkgs.gcc
    pkgs.zlib
  ];
}
