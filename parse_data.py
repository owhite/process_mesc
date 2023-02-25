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
        
def get_file_page(fname): # includes path
    try:
        f = open(fname, 'rb')
    except OSError:
        print ("Could not open/read file:", fname)
        sys.exit()

    with f:
        the_page = f.read()
        return(the_page)
        
def make_frame(page): 
    lines = page.splitlines();

    names = []
    sets = []
    i = 0

    for key in json.loads(lines[0]).keys():
        names.append(key)
        sets.append([])
        i = i + 1

    count = 0
    x = []
    for line in lines:
        js = json.loads(line)
        x.append(count)
        count = count + 1
        i = 0
        for n in names:
            sets[i].append(js[n])
            i = i + 1

    my_dict = {}
    i = 0
    for key in json.loads(lines[0]).keys():
        thing = {names[i]: sets[i]}
        my_dict.update(thing)
        i = i + 1
        
    return(my_dict)

