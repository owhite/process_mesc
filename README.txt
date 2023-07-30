Data Logging on the MP2

Introduction. My MP2 controller is located below the seat of my bike and quietly rests there as it's owner plots it's inevitable destruction. Many controllers have blown before it, usually through user error, or bad design. Yet somehow I have yet to manage to destroy this one. My next effort to send it into oblivion will be through overheating. Demise of the MP2 must be documented, lest it become like a tree falling in the forest that no one hears. Therefore I've constructed a data logger measure the state of the controller.

Data logger. A block diagram of the controller is here [LINK] and a picture of the board is here [LINK]. The circuit is not particularly interesting, and not well designed, so I'm not posting it. The main processor in the logger is based on a Teensy 4.1, which has an onboard SD card. I started with the teensy because they are very well supported, there's also an ESP32 on the logger which probably could have handled all of these activities. The logger has a SparkFun GPS Breakout which uses the NEO-M9N, and I had a MPU6050 module laying around to measure the bike's angle. I included a speaker for audio notification of when logging starts.

The logger uses the ESP32 as a serial repeater to connect between the teensy and a smartphone. The user can send commands using the "Serial bluetooth terminal" app on their android. Commands include record start, stop, and tweet (useful to know the thing is connect). Code on the teensy is here [LINK] and is based on the arduino framework in the platformio environment. The program running the logger operates as a simple state machine, is not particularly interesting, but one thing that took a bit of work was processing the data from the MP2 and is described next. 

MESC terminal. I cant say enough about how fantastic it is to receive data from the MP2 using MESC code. MESC firmware contains terminal program with very powerful capability. The terminal allows you to track data, change settings, store settings to non-volitle memory and reduces the number of times users need to recompile the MESC firmware. Users can connect to the MESC term from the USB port on the pill, or through pin connections off of the board. To enable my logger I needed to change this define:

#define HW_UART huart2

in MESC_F405RG/Core/Inc/MESC_F405.h

and settings of MESC_F405RG.ioc must be changed for UART3 on pins SOMETHING/SOMETHING using STM23cubeIDE. 

The MESC terminal has a number of extremely useful commands -- that richly deserve getting documented -- but for now, the two commands that will send data to the logger are _get_ and _status json_. The _get_ command produces a listing of all the settings for the MP2 that include Max Amps, Field Weakening Amps. _status json_ creates a stream of runtime variables from the MP2 such as phase Amps, battery voltage, throttle, and ehz. The logger sends the _get_ and _status json_ commands to the MP2, gathers the output from those commands, combines the runtime variables with input from the GPS and the MPU6050 accelerometer, and writes them to the onboard teensy SD card. Data is collected at 10 hz. 

Note 1: the MP2 also generates CAN output which is not used here.
Note 2: I was surprised that GPS data comes at 1hz.
Note 3: I used to send MP2 data directly to my phone via the ESP32 but I dont recommend this. There are known latency problems with bluetooth to androids and in my case it was dropping rows of information.

Heat generation and dissapation. We have documented building high amp boards here [https://github.com/badgineer/MP2-ESC/blob/main/docs/HIGHER_AMP_ASSEMBLY.md]. I use the big copper busbars, and in my case I am a big fan of 6mm thick laser cut aluminum heat sinks on the MOSFETs shown here:

https://github.com/badgineer/MP2-ESC/blob/main/gh_assets/HIGH_AMP_ASSEMBLY05.png
https://github.com/badgineer/MP2-ESC/blob/main/gh_assets/HIGH_AMP_ASSEMBLY06.png

Notice the use of high-temperature PEEK heatsink bolts for attaching the MOSFETs which I prefer over conductive bolts. The heat sinks are then bolted to an aluminum mounting plate. I drilled a 2mm hole into the aluminum heatsink plates and placed a rice-grain-sized thermistor for temp measurement there. 

Willful destruction of the MP2. The following is a plot of an XXX minute hill climb involving a change in elevation of YYY meters. The bike was described in a previous post [LINK]. Combined weight of me and the bike is ~130kg. 

Many thanks to @badgineer (MP2), @mxlemming (patience and MESC code), @netzpfuscher (MESC terminal), and Rob if youre out there (thermistor code). 


-------------------------------
Dependencies:
ffmpeg

Python modules:
mapplotlib
matplotlib
moviepy
pandas

-------------------------------

This fixed pytube to work on my mac

python -m pip install git+https://github.com/Zeecka/pytube@fix_1060
pip install --upgrade pytube

------------------------------
Making the video involves creating a series of videos that get stitched together. 
Be sure to check the output of every step, it is quite unlikely that everything will work the first time. The main thing to watch out for is if the codecs for audio and video work with ffmpeg, particularly when youre joining or overlaying videos together

## Go fetch the raw video footage from youtube
$ ./download_movie.py -c config.json -o raw.mp4

Get the resolution of the video, run:
$ ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 raw.mp4
1280x720

Get the duration of the video:
$ ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 raw.mp4
75.813152

These are configuration settings that go into config.json
    "movie_title": "MP2 hill climb",
    "amp_title": "FW=90, MAX=300A",
    "fig_height": 7,
    "fig_width": 10,
    "movie_URL": "https://youtu.be/UQB3h4kRCKc", 
    "movie_size": "1280x720", 
    "start_sec": 10.0, 
    "data_collection_period": 10.0, 
    "movie_duration": 75.81,
    "max_vals": 

fig_height/width refers to the size of the overlay on the raw video, the units are matplotlib units (inches?) and do not need to match the raw input video
movie_size is in pixels and does need to match the raw video
start_sec: your data probably does not go the whole length of the raw video, set this time point to when data was collected
max and min_vals refer to details of your controller

## Data overlay. Create a series of slides for overlay
#   note: this does not have to match the resolution of the raw video
#   note: this takes a while to run
$ ./bar_chart_overlay.py -d scrap.json -c config.json 

## use those slides to make transparent webm output
#  these types of steps could be done in the python programs but it's better to review
#  the intermediate results
$ ffmpeg -framerate 10 -pattern_type glob -i "images/*.png" -r 30  -pix_fmt yuva420p overlay.webm

## perform overlay of file output.webm on to thing.mp4
$ ffmpeg -i raw.mp4 -c:v libvpx-vp9 -i overlay.webm -filter_complex overlay movie.mp4

inspect movie.mp4 to make sure you have audio and an data overlay on top of the video. 

## create two pics then fade them in and out to create a movie
#   these are like opening credits and they need to be correct screen resolution
$ ./make_stats_slide.py -d scrap.json -c config.json -o premovie

## creates amp / ehz etc...
$ ./plot_amps.py -c config.json -d json_files/may21_1.json -o aftermovie

# This is how to create a still slide:
$ cat credits.txt | magick -gravity Center -background black -fill yellow -size 1280x720 -pointsize 24 label:@- credits.png

# This is how to convert a still slide into a fade in / fade out video:
$ ffmpeg -loop 1 -t 5 -i credits.png -filter_complex "[0:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v0];  [v0]concat=n=1:v=1:a=0,format=yuv420p[v]" -map "[v]" credits.mp4

# This is how to make a still slide of the WRONG size
$ cat credits.txt | magick -gravity Center -background black -fill yellow -size 1200x720 -pointsize 24 label:@- static.png

# make a video, this is the wrong size and will look like static in the last step.
$ ffmpeg -loop 1 -t 5 -i static.png -filter_complex "[0:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v0];  [v0]concat=n=1:v=1:a=0,format=yuv420p[v]" -map "[v]" static.mp4

$ ./combine.py output1.mp4 premovie.mp4 movie.mp4 aftermovie.mp4 credits.mp4 static.mp4


------------------------------
rpm(motor) = (ehz * 60) / pp
rpm(wheel) = (ehz * 60) / (pp * gear_ratio)
drpm(wheel) = rpm * circumference = (ehz * 60 * circumference) / (pp * 9.82)
drpm * minutes = distance traveled per minute = (dtpm)
dtpm = (ehz * 60 * circumference) / (pp * 9.82 * 60)
dtpms = (ehz * 60 * circumference) / (pp * 9.82 * 60 * 10)
circumference = 219.5
pp = 7
dtpms = (ehz * 60 * 219.5) / (7 * 9.82 * 60 * 10)
dtpms = ehz * (13170 / 41244)

distance traveled on a 219.5mm circuference tire for 1/10sec at given
dtpms = ehz * .31931 (cm)
dtpms = ehz * 3.1931 (mm)

