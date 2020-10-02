#!/bin/bash

mkdir ~/.aws
printf "[default]\naws_access_key_id = ${keyid}\naws_secret_access_key = ${keysecret}\n" > ~/.aws/credentials
printf "[default]\nregion=us-east-2\n" > ~/.aws/config
cat ~/.aws/credentials
exec $@