#! /usr/bin/python

import sys
import os
import json
import urllib
import requests

search_result_size = 500
saved_objects = { "dashboard": [], "index-pattern": [], "search": [], "visualization": [] }
current_directory = os.path.dirname(os.path.abspath(__file__))
elasticsearch_url = "http://127.0.0.1:9200"

if len(sys.argv) > 1:
   elasticsearch_url = sys.argv[1]

if len(sys.argv) > 2:
   search_result_size = sys.argv[2]

for object_type in saved_objects:
   object_directory = current_directory + '/' + object_type
   if not os.path.exists(object_directory):
       os.makedirs(object_directory)

for object_type, object_list in saved_objects.iteritems():
   object_search_url = elasticsearch_url + "/.kibana/_search?q=type:" + object_type + "&size=" + str(search_result_size)
   response = requests.get(url=object_search_url)
   json_data = response.json()
   object_search_data = json_data['hits']['hits']
   for item in object_search_data:
       object_id = item['_id']
       object_source =  item['_source']
       object_list.append(object_id)
       object_data_file = current_directory + '/' + object_type + '/' + object_id + ".json"
       outfile = open(object_data_file, "w")
       outfile.write(json.dumps(object_source, indent=4, sort_keys=True))
       outfile.close()
