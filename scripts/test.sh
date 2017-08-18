#!/bin/bash

export PATH="/opt/ghc/7.10.3/bin:$PATH"
export PATH="/opt/cabal/1.22/bin:$PATH"
export PATH="$HOME/.cabal/bin:$PATH"

git clone --depth 1 --recursive git://github.com/ghc/ghc
cd ghc
git clone https://github.com/izgzhen/hadrian
cd hadrian
git checkout staging
./build.cabal.sh selftest
./build.cabal.sh -j --verbose --no-progress --progress-colour=never --progress-info=brief --profile=-
./build.cabal.sh -j test --verbose --no-progress --progress-colour=never --progress-info=brief --profile=-
