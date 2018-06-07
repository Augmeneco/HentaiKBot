#!/bin/bash
#contents=$(cat ./config.json)
#echo "$(cat ./for_git/config.json)" > ./config.json
cp ./config.json ./config.json.tmp
cp ./for_git/config.json ./config.json
git commit -m "Какая-то говнокодная хуйня" -a
git push origin master
cp ./config.json.tmp ./config.json
rm ./config.json.tmp
#echo $contents > ./config.json