alias ga="git add -p"

alias gr="git fetch origin develop:develop && git rebase develop"
alias grs='need_stash=`git status --porcelain --untracked-files=no` && if [ -n "$need_stash" ]; then git stash; fi && git rebase -i --autosquash `git merge-base HEAD develop` && if [ -n "$need_stash" ]; then git stash pop; fi'

alias gp="git push origin HEAD"
alias gpf="gp -f"

alias ftn="cd ~/workspace/marvelscript/ && screen -c ~/.screen_envs/fountain"

export GIT_SSH_COMMAND='ssh -i ~/.ssh/id_personal_github_account -o IdentitiesOnly=yes'
export PS1="\[\e[32m\]\A\[\e[m\] \w \\$ "
export PATH="$PATH":"$HOME/.selfcompiledbins"
export EDITOR="emacsclient"

# For this to work, execute pipx install virtualenvwrapper and pipx install virtualenv
export VIRTUALENVWRAPPER_PYTHON=~/.local/pipx/venvs/virtualenvwrapper/bin/python
[ -f ~/.local/pipx/venvs/virtualenvwrapper/bin/virtualenvwrapper.sh ] && source ~/.local/pipx/venvs/virtualenvwrapper/bin/virtualenvwrapper.sh

export RUSTUP_HOME=~/.selfcompiledbins/rustup
export CARGO_HOME=~/.selfcompiledbins/cargo
export PATH="$PATH":"~/.selfcompiledbins/cargo/bin"

source "$HOME/local_bash_profile.sh"

# Never overwrite script files
alias script="script -a"

# For Binary installed with go installed
PATH="$PATH":$(go env GOPATH)"/bin"
