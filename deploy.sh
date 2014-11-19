#!/bin/sh
logya gen
git clone git@github.com:calisthenics/calisthenics.github.io.git
mv calisthenics.github.io/.git deploy/
cd deploy/
git add .
git commit -am 'new deployment'
git push
cd ..
rm -rf deploy/.git calisthenics.github.io/