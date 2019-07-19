#! /usr/bin/python

import os
import sys
import json
import urllib
import requests
import glob

current_directory = os.path.dirname(os.path.abspath(__file__))
object_templates_dir = current_directory
elasticsearch_url = "http://127.0.0.1:9200"

if len(sys.argv) > 1:
   object_templates_dir = sys.argv[1]

if len(sys.argv) > 2:
   elasticsearch_url = sys.argv[2]

object_templates = glob.glob(object_templates_dir + "/*.json")

for template in object_templates:
   object_id = template.replace(" ", "%20").split("/")[-1].split(".json")[0]
   add_object_cmd = 'curl -H "Content-Type: application/json" -XPUT "' + elasticsearch_url + '/.kibana/doc/' + object_id + '" -d "@' + template + '"'
   os.system(add_object_cmd)
