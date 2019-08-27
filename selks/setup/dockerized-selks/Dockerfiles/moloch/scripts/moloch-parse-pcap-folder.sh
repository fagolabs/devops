#!/bin/bash
cd /data/pcap/
#Parse all pcaps recursively only if they are a valid tcpdump capture
find . -exec file {} \; | grep "tcpdump capture" | awk -F: '{print $1}' | xargs -I % /data/moloch/bin/moloch-capture -r %
