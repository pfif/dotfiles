alias ga="git add -p"

alias gr="git fetch origin develop:develop && git rebase develop"
alias grs='need_stash=`git status --porcelain` && if [ -n "$need_stash" ]; then git stash; fi && git rebase -i --autosquash `git merge-base HEAD develop` && if [ -n "$need_stash" ]; then git stash pop; fi'

alias gp="git push origin HEAD"
alias gpf="gp -f"
