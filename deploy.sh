#!/bin/bash
set -euo pipefail

deploy_repo=~/repos/deploy/calisthenics.github.io

logya gen

rsync -aruvz --exclude=.git --exclude=.gitignore --delete deploy/ "$deploy_repo"

cd "$deploy_repo"
git add .
git commit -am'new deployment'
git push
