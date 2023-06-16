Duration needed:
181 - 67s = 114

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

