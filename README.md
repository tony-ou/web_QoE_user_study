
# README

## Description

These are source codes for setting up user study server AND analyze collected results .

Table of contents:
- Set up the environment
- Configure the server and host the survey page
- Analyze collected responses
- Demo of running mturk campaign + data analysis for "separate_poke2" campaign
- Previous webqoe experiments results
- Sensei data

## Set up the environment

1. Install `node.js` from its [official website](https://nodejs.org/en/download/)

   if you are using Windows, make sure to click 'add to path' when installing.

   if you want to run on the uchicago linux machine, follow their [guide to installing via binary archive](https://github.com/nodejs/help/wiki/Installation)

   To test if the installation is successful, you can input 

   ```shell
   node -v
   ```

   in your command line.

2. Download the zip file and unzip  it. Locate to the folder:

   ```shell
   cd web_QoE_user_study
   ```

3. (Optional) Install all the dependencies:

   This is an optional step for those without `node-modules` folder. If you have downloaded the complete file, all the modules are already in the `node-modules` folder.

   ```shell
   npm install
   ```


## Configure the server and host the survey page

RUN the following step on **farewell** machine if you want to start a mturk campaign. You can run this locally for debugging purpose (after starting server, you can see the page on localhost:PORT_NUM). But in order for mturkers to see your page, you must host the server online (You can use farewell or other tools like AWS EC2)

1. Fork a copy of this repo to your github. 
2. Change video url to your github video repo. The format is like: https://raw.githubusercontent.com/YOUR_GITHUB_ID/web_QoE_user_study/main/campaign/. 
   ```shell
   ./scripts/update_url.sh
   
   ```

3. Update campaign information (enter campaign name and number of test videos)
   ```shell
   ./scripts/update_campaign.sh 
   ```
 
4. Upload videos online (Follow https://github.com/tony-ou/web_QoE_video_creation/ to create test videos). Below shows you how to upload to github.
   ```shell
   mv path_of_video_folder ./campaign/
   git add campaign
   git commit -m 'upload videos'
   git push
   # Now you should see videos on YOUR_GITHUB_REPO_URL/CAMPAIGN_NAME/VIDEO_NUMBER.mp4
   ```
5. Start the server:

   ```shell
   node app.js [Optionally specify which port to run server; defaults to 3001 if not specified]
   ```

   If you run into any errors regarding modules not found, try removing the "node_modules" folder and go back to step 3.

6. You can access the page on `farewell.cs.uchicago.edu:3001` from outside machines.

   After finishing the test, the results will be stored in `./results/`, the file name will be the MTurk ID.
   
7. Other Tips:
   - Apart from Github, you can use Google Cloud Storage or Amazon S3 to store videos. Run script to change video url:
   ```shell
   ./scripts/update_url #use this to chagne video url to google storage/S3 url
   ```


## Analyze collected responses
1. Filter bad results (Check Point 4 for more instrucitons on how filtering works)
   ```shell
   python3 ./scripts/filter_results.py 
   ```

2. Create plots and logs. Plots are stored in ./fig, logs are in ./logs. This creates a standardized and a non-standardized plot, but we mostly only use standardized plot (exception check **old results** section). 
   ```shell
   ./scripts/get_results.sh 
   ```
3. Archive results before you start new experiments. Archived results are in ./old_results.
   ```shell
   ./scripts/move_results_out.sh 
   ```

4. Other Tips:

   - The raw data collected from the website are .txt files under `./results` (It contains grades, order of videos, watching and decision time of each grade, and the content of the survey, etc). Check `./controllers/start.js` `post_end` function to see what fields are written. 

   - You **MUST** archive results with `scripts/move_results_out.sh` because next campaign's results is also stored in `./results`. You will mix them up if you don't archive this campaign first. 

   - To revisit previous campaigns:
   ```shell
   ./scripts/move_results_in.sh 
   ```
   - Filtering: check filter_results.py for implementation. If you want to modify logic, edit the `filter_single_video` function.
   ```shell
   #Filtering logic. This is for a sample filtering for separate_poke2.   
   def filter_single_video(video_times, rating_times, video_order, scores,attentions):

       a = 0
       # check user finish the videos
       for k in video_times[:-1]:
           if k < 10000:
               a += 1
       if video_times[-1] < 7000:
           a +=1

       # check user rates reference video (3.mp4) highest
       if scores[-1] != max(scores):
           a+=1

       # check user responds 'yes' to attention check.
       if attentions[0] != 1:
           a += 1

       # reject if user fails any of the test
       if a > 0:
           return 1  #We reject this

       return 0 #We don't move this user to rejected folder

   ```

 

## Demo of running mturk campaign + data analysis for "separate_poke2" campaign

   ```shell
   # videos are already uploaded by me so you don't need to upload again.
   
   ./scripts/update_url.sh
   ENTER https://raw.githubusercontent.com/tony-ou/web_QoE_user_study/main/campaign/
   
   ./scripts/update_campaign.sh 
   First input: ENTER separate_poke2 
   Second input: ENTER 3

   node app.js
   # Now you should see the page on farewell.cs.uchicago.edu:PORT_NUM
   
   
   # Next for results analysis. results have been archived, you just need to pull them out. Make sure your results is empty before running these.
   
   ./scripts/move_results_in.sh
   ENTER separate_poke2
   
   python3 ./scripts/filter_results.py
   ./scripts/get_results.sh
   
   # Now you should see standardized plot named ./fig/separate_poke2_standardized_plot.png like below:
   ```
   
   ![sep](https://github.com/tony-ou/web_QoE_user_study/blob/main/fig/separate_poke2_standardized_plot.png)

## Previous webqoe experiments results

The results of previous web experiments are stored in in `./webqoe_previous_results`. Videos for these are experiments are in: https://drive.google.com/drive/u/0/folders/14OFi6iS2Eua4CPc4Dsi7KqotM12xkYwQ.


To load response files into results folder, run:
```
./scripts/move_results_in.sh
```

To put response files back to `./webqoe_previous_results`:
```
./scripts/move_results_out.sh
```

------
There are two experiments `separate_poke1` and `Almanac_mturk`, that  I accidentally deleted their response files. But you can still find their plots:   `./fig/separate_poke1_standardized_plot.png`,  `./fig/Almanac_mturk_standardized_plot.png`. And `Almanac_mturk` log file is also available `Almanac_mturk_results.log`. If you want to rerun these campaigns, the test videos are in https://drive.google.com/drive/u/0/folders/14OFi6iS2Eua4CPc4Dsi7KqotM12xkYwQ.

More details on these two experiments:
   - Separate_poke1: This experiment was run in paralell with `separate_poke2`. I collected ~40 responses in total for each experiment, and 30 responses remain after filtering. The hypothesis of these two experiments is to show the perception of the same delay depends on loading order of other objects. In both `separate_poke1`  and `separate_poke2`, video 2 has the same delay compared with video 1. But we wish loading of other objects make this delay more obvious in `separate_poke2` than in `separate_poke2`. The collected results confirmed this intuition: in `separate_poke1`, video 1 and video 2 have statistically similar user rating , while in separate_poke2, video 1 has higher rating than video 2.  
   - Almanac_mturk: The hypohtesis of this experiment is explained in 2.2 of my master thesis. 
  
## Sensei data
Sensei results are in `./sensei_results`. The test videos for sensei can be found:https://drive.google.com/drive/folders/1mmiawSmafU573t7MwfNBeTKdiNhCa4kO?usp=sharing . 

To load response files into results folder, run:
```
./scripts/move_sensei_results_in.sh
```

To put response files back to `./sensei_results`:
```
./scripts/move_sensei_results_out.sh
```

