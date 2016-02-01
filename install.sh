find ./ -name "*.*" -not -name "." -not -name ".git" -type d -exec cp -rv {} ~/ \;
find ./ -maxdepth 1 -name ".*" -type f -exec cp -v {} ~/ \;
