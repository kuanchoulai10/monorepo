# MacBook Development Environment Setup
Specs
- Apple M2
- 13.0 Ventura MacOS

## Install XCode Command Line Tools
Install Xcode Command Line Tools
```bash
xcode-select --install
```
- [What is the relationship between Xcode and Xcode command line tools?](https://apple.stackexchange.com/questions/150978/what-is-the-relationship-between-xcode-and-xcode-command-line-tools)

```bash
git config --global user.name <name>
git config --global user.email <email>

```

## Install [Homebrew](https://brew.sh/)

1. Install Homebrew
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   Homebrew files are installed into the `/opt/homebrew` folder (on Apple Silicon machines). But the folder is not part of the default `$PATH`.
2. After installed successfully, run these two commands in your terminal to add Homebrew to your `$PATH`:
   ```bash
   (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```
3. Turn Off Analytics
   ```bash
   brew analytics off
   ```
4. `brew doctor`

See [Install Homebrew](https://mac.install.guide/homebrew/3) for more information.


## Install [Oh My Zsh](https://ohmyz.sh/#install)
Oh My Zsh is an open source, community-driven framework for managing your Zsh configuration.

Install Oh My Zsh via `curl`:
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## Install Common Tools using Homebrew

[hashicorp/homebrew-tap](https://github.com/hashicorp/homebrew-tap)
```bash
brew tap hashicorp/tap
```

```bash
brew install $(cat formulae.txt)
```

```bash
brew install --cask $(cat casks.txt)
```

### [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#homebrew)

To activate the autosuggestions, add the following at the end of your `.zshrc`:

```bash
# zsh-autosuggestions.zsh
# https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
```

### [GitHub CLI](https://cli.github.com/)
```bash
gh auth login
```

### [nvm & Node.js](https://nodejs.org/en/download/package-manager/current)

add to `~/.zshrc`
```bash
# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion
```

```bash
nvm install --lts
```

### [`pipx`](https://pipx.pypa.io/stable/)

確認`pipx`所下載的app其執行檔位置有被加入至`PATH`環境變數中，若沒有則會加進去。
```
pipx ensurepath
```

- [使用 pipx 管理基於 Python 的 Command-Line 工具](https://josix.tw/post/pipx-deep-dive/)

### [`virtualenv`](https://virtualenv.pypa.io/en/latest/installation.html#via-pipx)

[User Guide](https://virtualenv.pypa.io/en/latest/user_guide.html)

```bash
pipx install virtualenv
mkdir ~/.venvs/
cd ~/.venvs/
virtualenv general --python python3.12
source ~/.venvs/general/bin/activate
```

### [`isort`](https://pycqa.github.io/isort/)

### [`bat`]

`.zshrc`:
```
alias cat="bat"
```

### [`fzf`]

`.zshrc`:

```
eval "$(fzf –zsh)"
```

### [`eza`]

`.zshrc`:

```
alias ls 
```