#!/bin/bash

export PATH="/opt/ghc/7.10.3/bin:$PATH"
export PATH="/opt/cabal/1.22/bin:$PATH"
export PATH="$HOME/.cabal/bin:$PATH"

sudo add-apt-repository ppa:hvr/ghc
sudo apt-get update
sudo apt-get install -y ghc-7.10.3 cabal-install-1.22 zlib1g-dev emacs dh-autoreconf ncurses-dev python-sphinx
git config --global url."git://github.com/ghc/packages-".insteadOf git://github.com/ghc/packages/
cabal update
cabal install alex happy ansi-terminal mtl shake quickcheck
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
