#!/bin/bash
# You have to rename ./secret-example to ./secret and fill in your connection data
source ./secret

#http://stackoverflow.com/a/12352101/1431660
#curl --data {"red":"00"} --digest -u "username:password" "http://localhost:3000/api/statistics"

curl --digest -u "$SWAPI_USER:$SWAPI_KEY" "$SWAPI_PROTO://$SWAPI_SERVER/api/articles"

# add new line:
echo