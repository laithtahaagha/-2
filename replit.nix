{pkgs}: {
  deps = [
    pkgs.postgresql
    pkgs.libxcrypt
    pkgs.libGLU
    pkgs.libGL
    pkgs.glibcLocales
    pkgs.freetype
  ];
}
