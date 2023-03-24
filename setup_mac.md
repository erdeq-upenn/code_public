# Set-up a new mac 
## Software
* MicroSoft Office
* Anaconda 
* python 
* github CLI
* Atom(sunsetted, use previous version)

## configs 
* bashrc  
```
alias ll='ls -a'
alias a1='ssh dsadmin@dsprod1.eastus.cloudapp.azure.com'
alias pp="python -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org "
alias work="cd /Users/dequan.er/Desktop/4-git/erdeq-upenn/"
```
* bash_profile
```
alias ll='ls -lhHG'
alias ls='ls -G'
alias a1='ssh dsadmin@dsprod1.eastus.cloudapp.azure.com'

if [ -f ~/.mygit ];then
    . ~/.mygit
fi
```
* bash_alias
```
alias a1='ssh dsadmin@dsprod1.eastus.cloudapp.azure.com'
```
* vimrc  
    - [installing pathogen](https://github.com/tpope/vim-pathogen)  Install to subdirectory under `~/.vim/bundle`  
    - [installing jedi](https://github.com/davidhalter/jedi-vim)  

my example mac `/.vimrc` file
```
" -------------------------------------
" vimrc for mac by Dequan Er, 2023
" -------------------------------------
syntax on         " highlighting
set nocompatible  " Use Vim defaults (even on Windows)
set noautoindent  " so that when we copy/paste the code - it doesn't move diagonally
set notitle       " to avoid vim renaming the title of the xterm window
set nonumber      " Don't show line numbers - I have them in status line
set ignorecase    " search case-insensitive (se ic, se noic)
set smartcase     " overrides the 'ignorecase' if search pattern contains capital character(s)
set incsearch     " search incremental
set hlsearch      " search highlighting (se hls, se nohls)
"set restorescreen " restore screen after you exit vim to what it was before you entered vim
"set equalalways   " set size of windows equal when creating windows with :new, :split, :vsplit
"set splitbelow    " open new window below the current one
" -------------------------------------
" use 4-space indentation
set tabstop=4     " read :help tab for explanation of tabstop, softtabstop, shiftwidth
set softtabstop=4 " tab
set shiftwidth=4  " tab width
set expandtab     " inserts spaces instead of tab (for real tab use ctrl-V followed by tab)
"set smarttab     " inserts spaces in the beginining, tabs in the middle, see :help smarttab
" -------------------------------------
" always show this custom status line
set laststatus=2  " always show status line
set statusline=%F%h%m%r%h%w%y\ %{&ff}\ ascii=\%03.3b\ hex=\%02.2B\ [%l,%v](%p%%\ of\ %L)(%o)\ %{strftime(\"%c\",getftime(expand(\"%:p\")))}%=\ 
set showtabline=2 " always show tabs
" -------------------------------------
" colors for vimdiff
if &diff
  highlight DiffAdd    ctermfg=black ctermbg=green
  highlight DiffDelete ctermfg=black ctermbg=grey
  highlight DiffChange ctermfg=black ctermbg=yellow
  highlight DiffText   ctermfg=black ctermbg=green
endif
" -------------------------------------
set cul
execute pathogen#infect()
let g:jedi#force_py_version = 3

```
* mygit  
```
#-- mygit
#    |-- gist 
#    |-- gd 
#    |-- mygc
#
# .mygit 
######################
# gd function
function gd(){
    # 1 file as parameter
    # show diff
    git fetch; git show origin/master:./$1 > ./$1.prev
    vimdiff -c 'syntax off' ./$1 ./$1.prev
    /bin/rm -f ./$1.prev
}

# gist function
function gist(){
    # 1 file as parameter
    # show diff in git 
    echo "---- file which diff from remote repo ----"
    git fetch 
    git diff --name-only origin/master .
    echo "---- file changed locally ----"
    git status .
    echo "------------------------------"
}

# mygc function
function mygc(){
    git add * 
    git commit -a -m "auto-update from NDR-mac $(date +%F-%T)"
    git push
}

```
## set-up brew/apt-get/wget
* [install brew](https://brew.sh/)  
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
* install wget  
```
brew install wget
```
## set-up git 
*  How to set up git on a new computer  
The new version of git removed https in `git fetch`, `git pull`. In order to use a repo with credentials, use the follwoing steps:
* [Generate new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
    - Use the Github email address to generate:
    `ssh-keygen -t ed25519 -C "your_email@example.com"`

    - Then add SSH key to ssh-agent
    Usinng `eval "$(ssh-agent -s)"`
    Then `touch ~/.ssh/config`
    then add into the `~/.ssh/config` file
    ```
    Host github.com
      AddKeysToAgent yes
      UseKeychain yes
      IdentityFile ~/.ssh/id_ed25519
    ```

    - Store SSH private key to the ssh-agent and keychain.
    ` ssh-add --apple-use-keychain ~/.ssh/id_ed25519`

* [Add a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## [set-up conda/pip ](https://pypi.org/project/pip/)

## [set-up virtualenv](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)
### virtualenv 
* Installation `pip install virtualenv`
* Usage: 
```
cd my-project/
virtualenv venv

virtualenv venv --system-site-packages # If you want your virtualenv to also inherit globally installed packages run

source venv/bin/activate

pip install <package>


...


deactivate
```
### [virtualwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
* install: `pip install virtualenvwrapper`  
* usage:  
1. Run: `workon`
2. A list of environments, empty, is printed.
3. Run: `mkvirtualenv temp`
4. A new environment, `temp` is created and activated.
5. Run: `workon`
6. This time, the `temp` environment is included.
