#!/bin/bash
echo "Checking ES"
until curl -sS "http://$ES_HOST:$ES_PORT/_cluster/health?wait_for_status=yellow"        
do                                                                                      
    echo "Waiting for ES to start"                                                      
    sleep 1                                                                             
done                                                                                    
#Wipe is the same initalize except it keeps users intact
echo WIPE | /data/moloch/db/db.pl http://$ES_HOST:$ES_PORT wipe
