#! /usr/bin/env python3

import json
import sys
import getopt
import subprocess
import parse_data # helper script

def manage_files():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"d:o:c:",["datafile=", "outputfile=", "config="])
    except getopt.GetoptError:
        print ('program.py -d <datafile> -o <output> -c <config>')
        sys.exit(2)

    dname = ""
    oname = ""
    cname = ""

    for opt, arg in opts:
        if opt in ("-d", "--datafile"):
            dname = arg
        if opt in ("-o", "--outputfile"):
            oname = arg
        if opt in ("-c", "--configfile"):
            cname = arg

    page = parse_data.get_json_file(dname)

    with open(cname, 'r') as fcc_file:
        config = json.load(fcc_file)

    return(page, config, oname)
    
# to run:
#   % ./make_stats_slide.py -d scrap.json -c config.json -o out4.mp4
# This grabs information from data, and from the config file
#   to create two still images, one with title and the other with stats. 
#   then it uses two pics fades them in and out to create a movie

def main():
    (page, config, output_file) = manage_files()

    blob = parse_data.load_get_response(page['blob'])
    values = ('curr_max', 'fw_curr', 'fw_ehz', 'i_max', 'p_max')

    tmp_file1 = "scrap1.png"
    tmp_file2 = "scrap2.png"

    str = ""
    str = "convert -background black -fill yellow  -size 600x300 -pointsize 60 -gravity Center label:\"" + config['title'] + "\" " + tmp_file1

    print("RUNNING: " + str)
    cp = subprocess.run([str], shell=True)

    str = ""
    for v in values:
        e = blob[v]
        e['desc'] = e['desc'].replace('weakenning', 'weakening')
        e['desc'] = e['desc'].replace('eHz under field weakening', 'field weakening eHz')
        e['desc'] = e['desc'].replace('max', 'Max')

        str = str + ('{} = {:d} ({})').format(e['desc'], int(float(e['value'])), v) + "\\n"

    str = "\"" + str + "\""
    str = "convert -background black -fill yellow  -size 600x300 -pointsize 30 -gravity Center label:" + str + " " + tmp_file2
    print("RUNNING: " + str)
    
    cp = subprocess.run([str], shell=True)

    str = "ffmpeg -loop 1 -t 5 -i " + tmp_file1 + " -loop 1 -t 5 -i " + tmp_file2 + " -filter_complex \"[0:v]fade=t=out:st=4:d=1[v0]; [1:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v1]; [v0][v1]concat=n=2:v=1:a=0,format=yuv420p[v]\" -map \"[v]\" " + output_file

    print("RUNNING: " + str)
    cp = subprocess.run([str], shell=True)

if __name__ == "__main__":
    main()






