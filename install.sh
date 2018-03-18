if output=$(git status --porcelain) && [ -z "$output" ]; then
    find ./ -maxdepth 1 -name "*" -not -name "." -not -name ".git" -type d -exec cp -rv {} ~/ \;
    find ./ -maxdepth 1 -name ".*" -not -name ".gitmodules" -type f -exec cp -v {} ~/ \;
else 
    echo "Clean that git directory"
    git status --porcelain
fi
