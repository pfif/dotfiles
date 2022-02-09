alias ga="git add -p"

alias gr="git fetch origin develop:develop && git rebase develop"
alias grs='need_stash=`git status --porcelain --untracked-files=no` && if [ -n "$need_stash" ]; then git stash; fi && git rebase -i --autosquash `git merge-base HEAD develop` && if [ -n "$need_stash" ]; then git stash pop; fi'

alias gp="git push origin HEAD"
alias gpf="gp -f"

alias ftn="cd ~/workspace/marvelscript/ && screen -c ~/.screen_envs/fountain"

export PS1="\[\e[32m\]\A\[\e[m\] \w \\$ "
export PATH="$PATH":"$HOME/.selfcompiledbins"

# For this to work, execute pipx install virtualenvwrapper and pipx install virtualenv
export VIRTUALENVWRAPPER_PYTHON=~/.local/pipx/venvs/virtualenvwrapper/bin/python
[ -f ~/.local/pipx/venvs/virtualenvwrapper/bin/virtualenvwrapper.sh ] && source ~/.local/pipx/venvs/virtualenvwrapper/bin/virtualenvwrapper.sh

if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi

source "$HOME/local_bash_profile.sh"

# Never overwrite script files
alias script="script -a"
