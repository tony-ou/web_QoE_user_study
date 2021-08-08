#!/bin/bash
echo "Enter url of videos. For example: https://raw.githubusercontent.com/tony-ou/web_QoE_user_study/main/campaign/"
read url
sed -i "/var video_url =/c\var video_url = path.join($url,vid_folder) + '/'" ../controllers/start
