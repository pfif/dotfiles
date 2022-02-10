export GIT_SSH_COMMAND='ssh -i ~/.ssh/id_personal_github_account -o IdentitiesOnly=yes'

# Waiting for a better solution that sulami/dotfiles is using
cp ~/.emacs.d/README.org ~/dotfiles/.emacs.d/README.org
git -C ~/dotfiles/ add -p
git -C ~/dotfiles/ commit
git -C ~/dotfiles/ push
