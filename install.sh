find ./ -maxdepth 1 -name "*" -not -name "." -not -name ".git" -type d -exec cp -rv {} ~/ \;
find ./ -maxdepth 1 -name ".*" -not -name ".gitmodules" -type f -exec cp -v {} ~/ \;
