# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import codecs
import json

"""
Your task in this exercise has two steps:
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import os

os.getcwd()
os.chdir('C:\Users\kaku\Desktop\project3_new')

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

double_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) 

lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')

expected = ["Tsawwassen","Park","Terminal"]
changes_required = { 'WEST BROADWAY': 'West Broadway',
           'east keith Road': 'East Keith Road',
           'Howe Street vancouver': 'Howe Street'
          } 
mapping = {'10': '10',
           '3305': '3305',
           '32500': '32500',
           '77A': '77A Avenue',
           '8500': '8500',
           '99': '99',
           'Alley': 'Alley',
           'Ave': 'Avenue',
           'Ave.': 'Avenue',
           'Blvd': 'Boulevard',
           'Broadway': 'Broadway',
           'Bypass': 'Bypass',
           'Centre': 'Centre',
           'Close': 'Close',
           'Crescent': 'Crescent',
           'Diversion': 'Diversion',
           'Dr': 'Drive',
           'Dr.': 'Drive',
           'East': 'East',
           'Edmonds': 'Edmonds Street',
           'Gate': 'Gate',
           'Grove': 'Grove',
           'Hastings': 'Hastings Street',
           'Highway': 'Highway',
           'Hwy': 'Highway',
           'Hwy.': 'Highway',
           'Kingsway': 'Kingsway',
           'Mall': 'Mall',
           'Mews': 'Mews',
           'Moncton': 'Moncton Street',
           'North': 'North',
           'Park': 'Park',
           'Pender': 'Pender Street',
           'RD': 'Road',
           'Rd': 'Road',
           'Rd.': 'Road',
           'Road,': 'Road',
           'S.': 'South',
           'Sanders': 'Sanders Street',
           'South': 'South',
           'St': 'Street',
           'St.': 'Street',
           'Street3': 'Street',
           'Terminal': 'Terminal',
           'Tsawwassen': 'North Tsawwassen',
           'Vancouver': 'Vancouver',
           'Walk': 'Walk',
           'Way': 'Way',
           'West': 'West',
           'Willingdon': 'Willingdon',
           'Wynd': 'Wynd',
           'av': 'Avenue',
           'road': 'Road',
           'st': 'Street',
           'street': 'Street',
           'Road':'Road',      
           'Street': 'Street',
           'Avenue': 'Avenue',
           'Drive': 'Drive',
           'Boulevard':'Boulevard',
           'Parkway': 'Parkway',
           'Place': 'Place',
           'Court': 'Court',
           'Trail': 'Trail',
           'Lane': 'Lane',
           'Jervis':'Jervis',
           'Broughton' :'Broughton',
           'Jarvis' : 'Jarvis',
           'East_8_Avenue' : 'East 8th Avenue',
           'east keith Road' : 'East Keith Road',
           'Howe Street vancouver': 'Howe Street'}

def update_name(name, mapping):
    
    match = re.search(street_type_re,name)
    if match:
        name = re.sub(street_type_re,mapping[match.group()],name)
    return name

file_in = 'vancouver_canada.osm' 
#file_in = 'sample.osm'
#file_in = 'example.osm'

def shape_element(element):
    
    if element.tag == "node" or element.tag == "way":
        node = {} 
        node['type'] = element.tag          
        for attrName, attrValue in element.attrib.items(): 
            if attrName == "lat":
                if 'pos' not in node.keys():
                    node['pos']= [float(1),float(1)]
                node['pos'][0] = float(attrValue)
                continue
            if attrName == "lon":
                if 'pos' not in node.keys():
                    node['pos']= [float(1),float(1)]
                node['pos'][1] = float(attrValue)
                continue
            if attrName == "" or attrValue == "": 
                continue
            if attrName == 'id': 
                node['_id'] = attrValue
            node[attrName] = attrValue
        #2nd level tags
        ndtags = element.findall("./*")
        for ndtag in ndtags:
            kvalue, vvalue, refvalue = ['','','']
            for aName, aValue in ndtag.attrib.items():
                if aName == "k":
                    kvalue = aValue
                if aName == "v":
                    vvalue = aValue
                if aName == "ref":
                    refvalue = aValue
            if kvalue == 'type': 
                continue
            dc,pc,lc = [double_colon.search(kvalue),problemchars.search(kvalue),lower_colon.search(kvalue)]
        
       
            if pc or dc: 
                continue 
            if vvalue in expected:
                continue
            if vvalue in changes_required: 
                vvalue = changes_required[vvalue]
            if kvalue.startswith("addr:"):
                if kvalue == "addr:street": 
                    vvalue = update_name(vvalue, mapping)         
                if 'address' not in node.keys(): 
                    node['address'] = {}
                node['address'][kvalue.split("addr:")[1]] = vvalue          
                continue
            if lc: 
                kvalue = re.sub(":"," ",kvalue) 
                node[kvalue] = vvalue
                continue
            if kvalue.startswith("geobase:"):  
                kvalue = kvalue.split("geobase:")[1] 
                node[kvalue] = vvalue
                continue                
            if kvalue == "" or vvalue == "": 
                continue
            if element.tag == "way" and refvalue != "" :  
                if "node_refs" not in node.keys():
                    node['node_refs'] = []
                node["node_refs"].append(refvalue)
            node[kvalue] = vvalue
       
        return node
    else:
        return None

def process_map(file_in, pretty = False):    
   
    file_out = "{0}.json".format(file_in)
    data = []
    counter = 0 
    with codecs.open(file_out, "w") as fo:        
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            counter += 1
            print counter
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
      
data = process_map(file_in, False)
