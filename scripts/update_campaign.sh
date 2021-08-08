#!/bin/bash
# A script to read results and return plots and a log

ls ./campaign

echo "Enter name of the campaign"
read camp

echo "Enter number of videos"
read num_vid

sed -i "/const vid_folder = /c\const vid_folder = '$camp\';" ../controllers/start
sed -i "/const num_vids =/c\const num_vids = $num_vid;" ../controllers/start
