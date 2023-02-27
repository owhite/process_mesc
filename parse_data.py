import urllib.request
import json

def get_web_page(req):
    try: urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        print(e.reason) 
    with urllib.request.urlopen(req) as response:
        the_page = response.read().decode('utf-8')
        response.close()
        return(the_page)
        
def get_json_file(fname):
    with open(fname, 'r') as fcc_file:
        the_page = json.load(fcc_file)
        return(the_page)

def make_frame(lines): 
    names = []
    sets = {}

    for key in lines[0].keys():
        names.append(key)
        sets[key] = []

    for line in lines:
        for name in names:
            sets[name].append(line[name])

    my_dict = {}
    for name in names:
        my_dict.update({name: sets[name]})
        
    return(my_dict)
