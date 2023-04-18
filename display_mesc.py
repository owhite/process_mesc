#! /usr/bin/env python3.11

import re

fake_get_response = """16:48:08.032 ^[[3`^[[36madc1_max^[[15`^[[37m| ^[[32m4080^[[35`^[[37m| 0^[[46`^[[37m| 4096^[[57`^[[37m| ADC1 max val
16:48:08.041 ^[[3`^[[36madc1_min^[[15`^[[37m| ^[[32m1200^[[35`^[[37m| 0^[[46`^[[37m| 4096^[[57`^[[37m| ADC1 min val
16:48:08.052 ^[[3`^[[36madc1_pol^[[15`^[[37m| ^[[32m1.000000^[[35`^[[37m| -1.00^[[46`^[[37m| 1.00^[[57`^[[37m| ADC1 polarity
16:48:08.062 ^[[3`^[[36madc2_max^[[15`^[[37m| ^[[32m4095^[[35`^[[37m| 0^[[46`^[[37m| 4096^[[57`^[[37m| ADC2 max val
16:48:08.068 ^[[3`^[[36madc2_min^[[15`^[[37m| ^[[32m1200^[[35`^[[37m| 0^[[46`^[[37m| 4096^[[57`^[[37m| ADC2 min val
16:48:08.079 ^[[3`^[[36madc2_pol^[[15`^[[37m| ^[[32m-1.000000^[[35`^[[37m| -1.00^[[46`^[[37m| 1.00^[[57`^[[37m| ADC2 polarity
16:48:08.095 ^[[3`^[[36madc_ext1^[[15`^[[37m| ^[[32m782^[[35`^[[37m| 0^[[46`^[[37m| 4096^[[57`^[[37m| Raw ADC throttle
16:48:08.109 ^[[3`^[[36mcurr_max^[[15`^[[37m| ^[[32m200.000000^[[35`^[[37m| 0.00^[[46`^[[37m| 300.00^[[57`^[[37m| Max motor current
16:48:08.125 ^[[3`^[[36mcurr_min^[[15`^[[37m| ^[[32m0.000000^[[35`^[[37m| -300.00^[[46`^[[37m| 0.00^[[57`^[[37m| Min motor current
16:48:08.136 ^[[3`^[[36mdirection^[[15`^[[37m| ^[[32m0^[[35`^[[37m| 0^[[46`^[[37m| 1^[[57`^[[37m| Motor direction
"""

# get string from terminal, remove vt100 characters, return tsv
def strip_vt100_commands (str):
    cmds = {
        '^[[32m': '',
        '^[[35m': '',
        '^[[36m': '',
        '^[[37m': '',
        '^[[46m': '',
        '^[[15': '',
        '^[[35': '',
        '^[[46': '',
        '^[[57': '',
        '^[[3': '', # put this last
        '`': ''}
    for key, value in cmds.items():
        str = re.sub('^[0-9: \.]*', '', str)
        str = str.replace(key, value)
        str = re.sub('\| ', '\t', str)

    return(str)

# 'get' returns a set of lines from term
#   process those and load into a dict
def load_get_response(lines):
    d = {}
    for line in lines.split('\n'):
        line = strip_vt100_commands(line)
        if (line.count('\t')) == 4: 
            l = line.split('\t');
            d[l[0]] = {}
            d[l[0]]['value'] = l[1]
            d[l[0]]['min']   = l[2]
            d[l[0]]['max']   = l[3]
            d[l[0]]['desc']  = l[4]
    return(d)

def run_command(cmd):
    str = ''
    if (cmd == 'get'):
        str = fake_get_response
    return(str)

s = run_command('get')
d = load_get_response(s)

print(d)
