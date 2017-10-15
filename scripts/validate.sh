#!/bin/bash

export PATH="/opt/ghc/7.10.3/bin:$PATH"
export PATH="/opt/cabal/1.22/bin:$PATH"
export PATH="$HOME/.cabal/bin:$PATH"
export PATH="/usr/local/bin:$PATH"

./build.sh -j --flavour=quickest validate --verbose
