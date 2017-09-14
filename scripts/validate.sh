#!/bin/bash

export PATH="/opt/ghc/7.10.3/bin:$PATH"
export PATH="/opt/cabal/1.22/bin:$PATH"
export PATH="$HOME/.cabal/bin:$PATH"
export PATH="/usr/local/bin:$PATH"

git clone --depth 1 --recursive git://github.com/ghc/ghc
cd ghc
git clone https://github.com/snowleopard/hadrian
cd hadrian
./build.cabal.sh -j --flavour=quickest validate --verbose
