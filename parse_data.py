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

def pad_data_set(array, speed, start_s, vid_len):
    key = list(array.keys())[0]
    row = array[key]
    data_sec = len(row) / speed
    end_sec = vid_len - start_s - data_sec
    front_pad = int(start_s * speed)
    end_pad = int(end_sec * speed)

    d = {}
    d['data'] = array
    d['front_pad']= front_pad
    d['data_len'] = len(row)
    d['end_pad']= end_pad

    for item in array:
        row = array[item]
        l1 = [row[0]] * front_pad
        l2 = [row[-1]] * end_pad
        array[item] = l1 + row + l2

    print('data length {0}(secs) {1}(frames)'.format(data_sec, len(row)))
    print('video length: {0}(secs) {1}(data_frames)'.format(vid_len, int(vid_len*speed)))
    print('adding {0}(secs) {1}(frames) to beginning'.format(start_s, front_pad))
    print('adding {0}(secs) {1}(frames) to end'.format(end_sec, end_pad))
    print('{0}(secs) {1}(frames) final dataset'.format(len(array[item]) / speed, len(array[item])))


    return(d)
