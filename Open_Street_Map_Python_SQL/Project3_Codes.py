
# coding: utf-8

# In[1]:

# Auditing Tags
"""
 This function reveals the type of tags (node, tag, nd, etc) and how many times it appears in the map.
 It takes as argument the file name and returns a dictionary with the tags and their counts
 
 """
import xml.etree.cElementTree as ET
import re

filename = 'san-francisco_california.osm'

def count_tags(filename):
    data = {}
    tree = ET.iterparse(filename)

    for n, element in tree:
        if element.tag not in data:
            data[element.tag] = 1
        else:
            data[element.tag]+=1
    
    return data


tags_dic = count_tags(filename)

print tags_dic


# In[2]:

# Auditing Street Name
"""
 This piece of code identifies if the tag is a street name. If it is, the function audit_streep_type takes as arguments a
 dictionary and the street name (Bancroft Way, Stockton Street, etc). 
 It returns a dictionary with the street types (Way, Street, etc) and their counts.
 """
from collections import defaultdict

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    


audit()


# In[3]:

# Exploring tags
"""
 This piece of code checks the "k" attribute for each "<tag>" in order to see if there are any potential problems.
 The key_type function takes as arguments a dictionary and a tag. 
 It returns a dictionary with the types of tags and their counts.
 Example of types of tags:
     lower: created_by
     lower_colon: census:population
     problemchars: addr.source:housenumber
     other: STATEFP
 """
import pprint

filename = 'san-francisco_california.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if re.search(lower, k):
            keys['lower']+=1
        elif re.search(lower_colon,k):
             keys['lower_colon']+=1
        elif re.search(problemchars,k):
             keys['problemchars']+=1
        else:
            keys['other']+=1
        
        
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


keys = process_map(filename)
pprint.pprint(keys)


# In[5]:

# Set of unique user id´s
"""To identify how many unique users have contributed to this map.
   The function process_map returns a set of unique user IDs ("uid")
 """
filename = 'san-francisco_california.osm'


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        dic = element.attrib
        if 'uid' in dic:
            users.add(dic['uid'])

    return users


users = process_map(filename)
pprint.pprint(users)
   


# In[ ]:

# Auditing City Name
"""
 This piece of code identifies if the tag is a city name. If it is, the function audit_city_name takes as arguments a
 dictionary and the city name (Albany, Berkeley, etc). 
 It returns a dictionary with the city names and their counts.
 """

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

filename = 'san-francisco_california.osm'

def audit_city_name(city_names, city_name):
    city_names[city_name] += 1
    
        


def is_street_city(elem):
    return (elem.attrib['k'] == "addr:city")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    city_names = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_city(tag):
                    audit_city_name(city_names, tag.attrib['v'])
    osm_file.close()
    return city_names


cty_names = audit(filename)
pprint.pprint(dict(cty_names))


# In[1]:

# Auditing Zip Codes
"""
 This piece of code identifies if the tag is a zip code. If it is, the function audit_zip_code takes as arguments a
 dictionary and the zip_code (94002,94044, etc). 
 It returns a dictionary with the zip codes and their counts.
 """
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

filename = 'san-francisco_california.osm'

    
def audit_zip_code(zip_codes, zip_code):
    zip_codes[zip_code] += 1

def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")   


def audit(osmfile):
    osm_file = open(osmfile, "r")
    zip_codes= defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zip_code(tag):
                    audit_zip_code(zip_codes, tag.attrib['v'])
    osm_file.close()
    return zip_codes


zp_codes = audit(filename)
pprint.pprint(dict(zp_codes))


# In[2]:

# Auditing State
"""
 This piece of code identifies if the tag is a state. If it is, the function audit_state takes as arguments a
 dictionary and the state name (California, CA, ca,etc). 
 It returns a dictionary with the state names and their counts.
 """
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

filename = 'san-francisco_california.osm'

def audit_state(states, state):
    states[state] += 1

def is_state(elem):
    return (elem.attrib['k'] == "addr:state")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    states= defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_state(tag):
                    audit_state(states, tag.attrib['v'])
    osm_file.close()
    return states



         
state_names = audit(filename)
pprint.pprint(dict(state_names))


# In[3]:

# Auditing Country
"""
 This piece of code identifies if the tag is a country name. If it is, the function audit_country takes as arguments a
 dictionary and the country name. It returns a dictionary with the country names and their counts. 
  """

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

filename = 'san-francisco_california.osm'

def audit_country(countries, country):
    countries[country] += 1

def is_country(elem):
    return (elem.attrib['k'] == "addr:country")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    countries= defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_country(tag):
                    audit_country(countries, tag.attrib['v'])
    osm_file.close()
    return countries



         
country_names = audit(filename)
pprint.pprint(dict(country_names))


# In[1]:

# Saving information on a CSV file
# Cleaning data inside the shape_element fuction
"""
    The purpose of this piece of code is to verify if the tag is a street name, city, postal code, state or country and to fix
    the fields that are problemtics.
    After fixing the information, it is saved on a csv file. There are 5 files and they have similar structures. 

"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

filename = 'san-francisco_california.osm'


NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

mapping_street = { "St": "Street",
            "St.": "Street",
           "street": "Street",
           "st":"Street",
           "AVE": "Avenue",
           "Ave": "Avenue",
           "Ave.":"Avenue",
           "Avenie": "Avenue",
           "avenue": "Avenue",
           "blvd":"Boulevard",
           "Blvd": "Boulevard",
           "Blvd.":"Boulevard",
           "Blvd,":"Boulevard",
           "Dr":"Drive",
           "Dr.":"Drive",
           "Pl":"Place",
           "square":"Square",
           "Rd":"Road",
           "Rd.": "Road",
           "parkway":"Parkway",
           "way":"Way",
           "broadway":"Broadway",
           "Hwy":"Highway",
           "I-580)":"I-580"
            }           

mapping_city = { "alameda": "Alameda",
            "Alamda": "Alameda",
           "Artherton": "Atherton",
           "Berkeley, CA":"Berkeley",
                "berkeley":"Berkeley",
                "Emeyville":"Emeryville",
                "Fremont ":"Fremont",
                "OAKLAND":"Oakland",
                "Oakland ":"Oakland",
                "Oakland CA":"Oakland",
                "Oakland, CA":"Oakland",
                "Oakland, Ca":"Oakland",
                "Okaland":"Oakland",
                "oakland":"Oakland",
                "Pleasant Hill, CA":"Pleasant Hill",
                "San Francicsco":"San Francisco",
                "san Francisco":"San Francisco",
                "san francisco":"San Francisco",
                "Sausalito ":"Sausalito",
                "daly City":"Daly City",
                "hayward":"Hayward",
                "san Carlos":"San Carlos",
                "san Mateo":"San Mateo",
                "south San Francisco":"South San Francisco",
                "walnut Creek":"Walnut Creek"}

mapping_state = { "Ca": "CA",
            "ca": "CA",
           "California": "CA"}

mapping_country = { "UA": "US"}

def update_zip_code( zip_code):
    clean_postcode = re.match(r'^(\d{5})', zip_code)
    if clean_postcode:
        return clean_postcode[0]
    clean_postcode1 = re.findall(r'^(\d{5})-\d{4}$', zip_code)
    if clean_postcode1:
        return clean_postcode1[0]
    else:
        return []

def update_city(city, mapping_city):
    city_name = city
    if city in mapping_city:
        rep = mapping_city[city]
        city_name = city_name.replace(city,rep)
    return city_name
        
def update_name(name, mapping_street):
    s = re.search(street_type_re,name)
    if s:
        smt =s.group()
        if smt in mapping_street:
            rep = mapping_street[smt]
            name = name.replace(smt,rep)
    return name

def update_state(state, mapping_state):
    state_name = state
    if state in mapping_state:
        rep = mapping_state[state]
        state_name = state_name.replace(state,rep)
    return state_name

def update_country(country, mapping_country):
    country_name = country
    if country in mapping_country:
        rep = mapping_country[country]
        country_name = country_name.replace(country,rep)
    return country_name

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag =='node':
        for item in node_attr_fields:
            if item not in element.attrib:
                return {'node': node_attribs, 'node_tags': tags}
                
        
        for num in node_attr_fields:
                node_attribs[num] = element.attrib[num]
        
            
                    
        for tag in element.iter("tag"):
            k = tag.attrib['k']
            if re.search(problem_chars,k): continue
            dic = {} 
            if k=="addr:street":
                dic['value'] = update_name(tag.attrib['v'], mapping_street)
            elif k=="addr:city":
                dic['value'] = update_city(tag.attrib['v'], mapping_city)
            elif k=="addr:state":
                dic['value'] = update_state(tag.attrib['v'], mapping_state)
            elif k=="addr:country":
                dic['value'] = update_country(tag.attrib['v'], mapping_country)
            elif k=="addr:postcode":
                var = update_zip_code(tag.attrib['v'])
                if len(var)>0:
                    dic['value'] = var
                else: continue
                
            else:
                dic['value'] = tag.attrib['v']
           
            dic['id'] = element.attrib['id']
            colon = re.search(LOWER_COLON, k)
            if colon:
                words = tag.attrib['k'].split(':')
                if len(words)==2:
                    dic['key'] =  words[1]
                    dic['type'] = words[0]
                elif len(words)==3:
                    dic['key'] =  words[1]+':'+words[2]
                    dic['type'] = words[0]
            else:
                dic['key'] =  tag.attrib['k']
                dic['type'] = default_tag_type
            
            tags.append(dic)
    else:
        for number in way_attr_fields:
            way_attribs[number] = element.attrib[number]
        
            position = 0
        for w_node in element.iter("nd"):
            way_dic = {}
            
            way_dic['id'] = element.attrib['id']
            way_dic['node_id'] = w_node.attrib['ref']
            way_dic['position'] = position
            position+=1
            way_nodes.append(way_dic)
            
        for way_node in element.iter("tag"):
            kt = way_node.attrib['k']
            if re.search(problem_chars,kt): continue
            dic_ = {}
            if kt=="addr:street":
                dic_['value'] = update_name(way_node.attrib['v'], mapping_street)
            elif kt=="addr:city":
                dic_['value'] = update_city(way_node.attrib['v'], mapping_city)
            elif kt=="addr:state":
                dic_['value'] = update_state(way_node.attrib['v'], mapping_state)
            elif kt=="addr:country":
                dic_['value'] = update_country(way_node.attrib['v'], mapping_country)
            elif kt=="addr:postcode":
                var = update_zip_code(way_node.attrib['v'])
                if len(var)>0:
                    dic_['value'] = var
                else: continue
            else:
                dic_['value'] =  way_node.attrib['v']
            
            dic_['id'] = element.attrib['id']
            colon = re.search(LOWER_COLON, kt)
            if colon:
                words = way_node.attrib['k'].split(':')
                if len(words)==2:
                    dic_['key'] =  words[1]
                    dic_['type'] = words[0]
                elif len(words)==3:
                    dic_['key'] =  words[1]+':'+words[2]
                    dic_['type'] = words[0]
            else:
                dic_['key'] =  way_node.attrib['k']
                dic_['type'] = default_tag_type
            
            tags.append(dic_)
            
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()
        

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

process_map(filename)


# In[ ]:

# FROM CSV TO SQL DATABASE


# In[2]:

# Creating the database and tables
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS nodes_tags;
DROP TABLE IF EXISTS ways;
DROP TABLE IF EXISTS ways_tags;
DROP TABLE IF EXISTS ways_nodes;

CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);''')

conn.commit()


# In[3]:

# Importing CSV content into nodes table
"""
    Before inserting the information into the tables, it is necessary that the type of the data match the type required by the
    table.Even after the data cleaning, the csv files contain some blank lines, which brake the code. 
    So, I inserted a try/except clause in order to solve it. 
    The example below is from nodes.csv file, but the other four work the same way.
"""
import csv, sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

with open('nodes.csv','rb') as filename:
    reader = csv.DictReader(filename)
    for row in reader:
        try:
            id_ = int(row['id'])
            lat = float(row['lat'])
            lon= float(row['lon'])
            user = row['user'].decode("utf-8")
            uid = int(row['uid'])
            version = int(row['version'])
            changeset = int(row['changeset'])
            timestamp = row['timestamp']
        except:
            continue
        
        
        cur.execute('''INSERT OR IGNORE INTO nodes (id,lat,lon,user,uid,version,changeset,timestamp) 
        VALUES ( ?, ?,?,?,?,?,?,? )''', ( id_,lat,lon,user,uid,version,changeset,timestamp ) )
        

    conn.commit()
    conn.close()



# In[4]:

# Importing CSV content into nodes_tags table
import csv, sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

with open('nodes_tags.csv','rb') as filename:
    reader = csv.DictReader(filename)
    for row in reader:
        try:
            id_ = int(row['id'])
            value = row['value'].decode("utf-8")
            key = row['key']
            type_ = row['type']
        except:
            continue
        
        
        cur.execute('''INSERT OR IGNORE INTO nodes_tags (id,key,value,type) 
        VALUES ( ?, ?,?,?)''', ( id_,key,value,type_ ) )
        

    conn.commit()
    conn.close()


# In[5]:

# Importing CSV content into ways table

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

with open('ways.csv','rb') as filename:
    reader = csv.DictReader(filename)
    for row in reader:
        try:
            id_ = int(row['id'])
            user = row['user'].decode("utf-8")
            uid = int(row['uid'])
            version = row['version']
            changeset = int(row['changeset'])
            timestamp = row['timestamp']
        except:
            continue
        
        
        cur.execute('''INSERT OR IGNORE INTO ways (id,user,uid,version,changeset,timestamp) 
        VALUES ( ?, ?,?,?,?,?)''', ( id_,user,uid,version,changeset,timestamp ) )
        

    conn.commit()
    conn.close()


# In[6]:

# Importing CSV content into ways_tags table

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

with open('ways_tags.csv','rb') as filename:
    reader = csv.DictReader(filename)
    for row in reader:
        try:
            id_ = int(row['id'])
            value = row['value'].decode("utf-8")
            key = row['key']
            type_ = row['type']
        except:
            continue
        
        
        cur.execute('''INSERT OR IGNORE INTO ways_tags (id,key,value,type) 
        VALUES ( ?, ?,?,?)''', ( id_,key,value,type_ ) )
        

    conn.commit()
    conn.close()


# In[7]:

# Importing CSV content into ways_nodes table

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

with open('ways_nodes.csv','rb') as filename:
    reader = csv.DictReader(filename)
    for row in reader:
        try:
            id_ = int(row['id'])
            node_id = int(row['node_id'])
            position = int(row['position'])
        except:
            continue
        
        
        cur.execute('''INSERT OR IGNORE INTO ways_nodes (id,node_id, position) 
        VALUES ( ?, ?,?)''', ( id_,node_id, position) )
        

    conn.commit()
    conn.close()


# In[8]:

# Queries: Number of Nodes and Ways
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

Query = "SELECT COUNT(*) FROM nodes;"
cur.execute(Query)
rows = cur.fetchall()


for row in rows:
    print "Number of nodes:", row[0]

Query_1 = "SELECT COUNT(*) FROM ways;"
cur.execute(Query_1)
lines = cur.fetchall()

for line in lines:
    print "Number of ways: ", line[0]
    
    
    
conn.close()


# In[9]:

# Query: Number of Unique Users

import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

Query = "SELECT COUNT(DISTINCT(all_nodes.uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) as all_nodes;"
cur.execute(Query)
users = cur.fetchall()

for user in users:
    print "Number of unique users: ", user[0]

conn.close()


# In[10]:

# Query: 10 Users that most contributed to the map

import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

Query = "SELECT all_nodes.user, COUNT(*) as count FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as all_nodes GROUP BY all_nodes.user ORDER BY count DESC limit 10;"
cur.execute(Query)
users = cur.fetchall()

for user in users:
    print user[0], user[1]

conn.close()


# In[11]:

# Query: 10 most common cities in the map
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

Query = "SELECT all_tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) as all_tags WHERE all_tags.key=='city' GROUP BY all_tags.value ORDER BY count DESC limit 10;"
cur.execute(Query)
cities = cur.fetchall()

for city in cities:
    print city[0], city[1]

conn.close()


# In[13]:

# Query: most common zip codes in the map
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

QUERY = "SELECT all_tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) as all_tags WHERE all_tags.key='postcode'GROUP BY all_tags.value ORDER BY count DESC limit 10;"
cur.execute(QUERY)
zipcodes = cur.fetchall()

for zipcode in zipcodes:
    print zipcode[0], zipcode[1]

conn.close()


# In[14]:

# Query: most common streets
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

QUERY = "SELECT all_tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) as all_tags WHERE all_tags.key='street'GROUP BY all_tags.value ORDER BY count DESC limit 10;"
cur.execute(QUERY)
streets = cur.fetchall()
for street in streets:
    print street[0], street[1]

conn.close()


# In[15]:

# Query: Types of amenities
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

QUERY = "SELECT all_tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) as all_tags WHERE all_tags.key='amenity'GROUP BY all_tags.value ORDER BY count DESC limit 10;"
cur.execute(QUERY)
amen = cur.fetchall()
for am in amen:
    print am[0], am[1]

conn.close()


# In[16]:

# Query: Popular cuisines
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

QUERY = "SELECT all_tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) as all_tags WHERE all_tags.key='cuisine'GROUP BY all_tags.value ORDER BY count DESC limit 10;"
cur.execute(QUERY)
restaurants = cur.fetchall()
for rest in restaurants:
    print rest[0], rest[1]

conn.close()


# In[17]:

# Query: Sources of Information
import sqlite3

conn = sqlite3.connect('project3.sqlite')
cur = conn.cursor()

QUERY = "SELECT all_tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) as all_tags WHERE all_tags.key='source'GROUP BY all_tags.value ORDER BY count DESC limit 10;"
cur.execute(QUERY)
sources = cur.fetchall()

for source in sources:
    print source[0], source[1]

conn.close()


# In[ ]:



