#! /usr/bin/env python3

import moviepy.editor as mp

video = mp.VideoFileClip("dummy2.mp4");

logo = (mp.ImageClip("thing.png")
          .set_duration(video.duration)
          .resize(height=200) # if you need to resize...
          .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
          .set_pos(("right","top")))

final = mp.CompositeVideoClip([video, logo])
final.write_videofile("test.mp4")