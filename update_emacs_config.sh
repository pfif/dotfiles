# Waiting for a better solution that sulami/dotfiles is using
cp ~/.emacs.d/README.org ~/dotfiles/.emacs.d/README.org
git -C ~/dotfiles/ add -p
git -C ~/dotfiles/ commit
git -C ~/dotfiles/ push
