alias ga="git add -p"

alias gr="git fetch origin develop:develop && git rebase develop"
alias grs='need_stash=`git status --porcelain --untracked-files=no` && if [ -n "$need_stash" ]; then git stash; fi && git rebase -i --autosquash `git merge-base HEAD develop` && if [ -n "$need_stash" ]; then git stash pop; fi'

alias gp="git push origin HEAD"
alias gpf="gp -f"

alias ftn="cd ~/workspace/marvelscript/ && screen -c ~/.screen_envs/fountain"

#WORK SPECIFICS
alias vu="vagrant up; vagrant ssh"
alias raise='if_stmt="if self.bubble_exceptions()"; toggle=" or True"; file="/Users/florentpastor/Documents/ostmodern/ost-skylark/skylark/core/api.py"; if [ -n "`grep "$if_stmt$toggle" $file`" ]; then sed -i.bak "s/$if_stmt$toggle/$if_stmt/" $file; echo $if_stmt; else sed -i.bak "s/$if_stmt/$if_stmt$toggle/" $file; echo $if_stmt$toggle; fi'

cd ~/Documents/ostmodern/ost-skylark/
