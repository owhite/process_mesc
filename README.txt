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

------------------------------

This fixed pytube to work on my mac

python -m pip install git+https://github.com/Zeecka/pytube@fix_1060
pip install --upgrade pytube

------------------------------
## create a series of slides for overlay
$ ./bar_chart_overlay.py -d scrap.json -c config.json 

## use those slides to make transparent webm output
$ ffmpeg -framerate 10 -pattern_type glob -i "images/*.png" -r 30  -pix_fmt yuva420p output.webm

## retreive youtube video
$ ./download_movie.py -c config.json -o thing.mp4

## perform overlay of file output.webm on to thing.mp4
$ ffmpeg -i thing.mp4 -c:v libvpx-vp9 -i output.webm -filter_complex overlay output.mp4

## create two pics then fade them in and out to create a movie
$ ./make_stats_slide.py -d scrap.json -c config.json -o test

## creates amp / ehz etc...
$ ./plot_amps.py -c config.json -d json_files/may21_1.json -o thing.png

NOT WORKING: 
$ ffmpeg -i "test.mp4" -f lavfi -i aevalsrc=0 -shortest -y "new_test.mp4"
$ ffmpeg -i "output.mp4" -f lavfi -i aevalsrc=0 -shortest -y "new_output.mp4"

$ ffmpeg -f concat -safe 0 -i new_test.mp4 -i new_output.mp4 -c copy output2.mp4
$ ffmpeg -i new_test.mp4 -i new_output.mp4 -f concat -safe 0 -c copy output2.mp4

ffmpeg -i "concat:new_test.mp4|new_output.mp4" -c copy output10.mp4

------------------------------
LOTS OF OLD FFMPEG ATTEMPTS:

Use this in scroll_plot to stretch to correct duration
writervideo = animation.FFMpegWriter(fps=8.18)

I think this changes framerate
ffmpeg -i process_mesc/druid_hill_climb2.mp4 -filter:v fps=fps=60 output1.mp4

you made a dummy version of the scroll that does not move. 
ffmpeg -i process_mesc/dummy.mp4 -filter:v fps=fps=60 output2.mp4

Get 67 seconds of that, trim to length
$ ffmpeg -ss 00:00:00 -to 00:01:06 -i output2.mp4 -c copy output3.mp4

echo '# videos.txt' > list.txt
echo 'file output3.mp4' >> list.txt
echo 'file output1.mp4' >> list.txt
echo 'file output3.mp4' >> list.txt

ffmpeg -f concat -safe 0 -i list.txt -c copy output4.mp4

$ ffmpeg -i output.mp4  -filter:v fps=fps=60 scrap1.mp4

$ ffmpeg -i output4.mp4 -f mov output_file2.mov
$ ffmpeg -i Downloads/druid_hill_climb2.MP4 -f mov output_file1.mov
$ ffmpeg -i output_file1.mov -i output_file2.mov  -vsync 2 -filter_complex vstack=inputs=2:shortest=1 thing.mov

$ ffmpeg -i output_file1.mov -i output_file2.mov  -vsync 2 -filter_complex vstack=inputs=2:shortest=1 thing.mov

# makes an mp4
ffmpeg -pattern_type glob -i 'images/*.jpg' movie.mp4

change duration
ffmpeg -i input.mp4 -filter_complex "setpts=PTS/(120/30);atempo=120/30" output.mp4

cat [file with data goes here] | convert -background black xc:none -fill yellow  -size 600x300 -pointsize 30 -gravity Center label:@- thing.jpeg

cat *.png | ffmpeg -y -f image2pipe -r 30 -i - -c:v libvpx -pix_fmt yuva420p -metadata:s:v:0 alpha_mode="1"  output.webm

make webm output, also
ffmpeg -framerate 10 -i images/%03d.png -c:v libvpx-vp9 -pix_fmt yuva420p output.webm

** ffmpeg -framerate 10 -pattern_type glob -i 'images/*.png' -c:v libvpx-vp9 -pix_fmt yuva420p output.webm

** % ./pytube_test.py 

overlay
ffmpeg -i druid_hill_climb2.mp4 -i movie.mp4 -filter_complex overlay output.mp4

another overlay
ffmpeg -y -i druid_hill_climb2.mp4 -i movie.mp4 -filter_complex [1]format=rgb24,colorkey=black,colorchannelmixer=aa=0.3,setpts=PTS+8/TB[1d]; [0][1d]overlay=enable='between(t,8, 13)'[v1]; -map [v1] -map 0:a -c:a copy -c:v libx264 -preset ultrafast output.mp4

