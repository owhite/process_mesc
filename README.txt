Duration needed:
181 - 67s = 114

### make transparent webm output
ffmpeg -framerate 10 -pattern_type glob -i "images/*.png" -r 30  -pix_fmt yuva420p output.webm

## then, overlay webm on mp4
ffmpeg -i druid_hill_climb2.mp4 -c:v libvpx-vp9 -i output.webm -filter_complex overlay output.mp4



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



cat *.png | ffmpeg -y -f image2pipe -r 30 -i - -c:v libvpx -pix_fmt yuva420p -metadata:s:v:0 alpha_mode="1"  output.webm

make webm output, also
ffmpeg -framerate 10 -i images/%03d.png -c:v libvpx-vp9 -pix_fmt yuva420p output.webm

overlay
ffmpeg -i druid_hill_climb2.mp4 -i movie.mp4 -filter_complex overlay output.mp4

another overlay
ffmpeg -y -i druid_hill_climb2.mp4 -i movie.mp4 -filter_complex [1]format=rgb24,colorkey=black,colorchannelmixer=aa=0.3,setpts=PTS+8/TB[1d]; [0][1d]overlay=enable='between(t,8, 13)'[v1]; -map [v1] -map 0:a -c:a copy -c:v libx264 -preset ultrafast output.mp4
