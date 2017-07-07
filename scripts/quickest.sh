#!/bin/bash

git clone --depth 1 --recursive git://github.com/ghc/ghc
cd ghc
git clone https://github.com/snowleopard/hadrian
cd hadrian
./build.sh selftest
./build.sh -j --flavour=quickest --verbose --no-progress --progress-colour=never --progress-info=brief --profile=-
