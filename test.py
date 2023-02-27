#! /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import parse_data # helper script

fname = 'datasets/test.json'

the_page = parse_data.get_json_file(fname)
print (the_page['title'])

data = parse_data.make_frame(the_page['data'])
df = pd.DataFrame(data)

print (df)
