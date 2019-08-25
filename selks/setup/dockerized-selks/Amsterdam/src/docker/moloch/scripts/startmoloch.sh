#!/bin/sh

echo "Giving ElasticSearch time to start..."
sleep 10
until curl -sS "http://$ES_HOST:$ES_PORT/_cluster/health?wait_for_status=yellow"
do
    echo "Waiting for ES to start"
    sleep 1
done
echo
#Configure Moloch to Run
if [ ! -f /data/configured ]; then
	touch /data/configured
	/data/moloch/bin/Configure
fi
#Give option to init ElasticSearch
if [ "$INITALIZEDB" = "true" ] ; then
	echo INIT | /data/moloch/db/db.pl http://$ES_HOST:$ES_PORT init
	/data/moloch/bin/moloch_add_user.sh $MOLOCH_ADMIN_USER "SELKS Admin User" $MOLOCH_PASSWORD --admin
        echo "\n### Setting up Scirius/Moloch proxy user ###\n"
        cd /data/moloch/viewer
        /data/moloch/bin/node addUser.js -c /data/moloch/etc/config.ini moloch moloch moloch --admin --webauth
fi
#Give option to wipe ElasticSearch
if [ "$WIPEDB" = "true" ]; then
	/data/wipemoloch.sh
fi

echo "Look at log files for errors"
echo "  /data/moloch/logs/viewer.log"
echo "  /data/moloch/logs/capture.log"
echo "Visit http://127.0.0.1:8005 with your favorite browser."
echo "  user: $MOLOCH_ADMIN_USER"
echo "  password: $MOLOCH_PASSWORD"

if [ "$CAPTURE" = "on" ]
then
    echo "Launch capture..."
    if [ "$VIEWER" = "on" ]
    then
        # Background execution
        $MOLOCHDIR/bin/moloch-capture >> $MOLOCHDIR/logs/capture.log 2>&1 &
    else
        # If only capture, foreground execution
        $MOLOCHDIR/bin/moloch-capture |tee -a $MOLOCHDIR/logs/capture.log 2>&1
    fi
fi

if [ "$VIEWER" = "on" ]
then
    echo "Launch viewer..."
   /bin/sh -c 'cd $MOLOCHDIR/viewer; $MOLOCHDIR/bin/node viewer.js -c $MOLOCHDIR/etc/config.ini | tee -a $MOLOCHDIR/logs/viewer.log 2>&1' 
fi 

