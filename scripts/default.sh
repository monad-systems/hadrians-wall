#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PATH="/opt/ghc/7.10.3/bin:$PATH"
export PATH="/opt/cabal/1.22/bin:$PATH"
export PATH="$HOME/.cabal/bin:$PATH"
export PATH="/usr/local/bin:$PATH"

./build.sh selftest
./build.sh -j --verbose --no-progress --progress-colour=never --progress-info=brief --profile=-
./build.sh -j --verbose --no-progress --progress-colour=never --progress-info=brief --profile=- --install-destdir=$PWD install

$PWD/usr/local/bin/ghc $SCRIPT_DIR/Test.hs
$PWD/usr/local/bin/ghc -dynamic --make $SCRIPT_DIR/Test.hs
