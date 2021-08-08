
# README

## Description

These are source codes for setting up user study server AND analyze collected results .

## Setup

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

## Create test videos
Follow https://github.com/tony-ou/web_QoE_video_creation/ to create test videos. 

## Configure the server and publish it
RUN the following step on **farewell** machine if you want to start an mturk campaign. You can run this locally for debugging purpose (you see the page on localhost:PORT_NUM). But in order for mturkers to see your page, you must host the server online. You can use farewell or other tools like AWS EC2

1. Change video url to your github video repo 
   ```shell
   ./scripts/update_url.sh
   ```

2. Update campaign information (campaign name and number of test videos)
   ```shell
   ./scripts/update_campaign.sh 
   ```
 
3. Upload videos online. Below shows you how to upload to github. You should be able to access videos via:https://raw.githubusercontent.com/YOUR_GITHUB_ID/web_QoE_user_study/main/campaign/video_folder_name/video_number.mp4
   ```shell
   mv path_to_videos ./campaign/
   git add campaign
   git commit -m 'upload videos'
   git push
   ```
4. Start the server:

   ```shell
   node app.js [Optionally specify which port to run server; defaults to 3001 if not specified]
   ```

   If you run into any errors regarding modules not found, try removing the "node_modules" folder and go back to step 3.

5. You can access the page on `farewell.cs.uchicago.edu:3001` from outside machines.

   After finishing the test, the results will be stored in `./results/`, the file name will be the MTurk ID.
   
6. Other Tips:
   - Apart from Github, you can use Google Cloud Storage or Amazon S3 to store videos. Run script to change video url:
   ```shell
   ./scripts/update_url #use this to chagne video url to google storage/S3 url
   ```


## Analyze data
1. Filter bad results
   ```shell
   python3 ./scripts/filter_results.py 
   ```

2. Create plots and logs (plots are stored in ./fig, logs are in ./logs) 
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
   
   # Now you should see standardized plot created in ./fig like below:
   ```
   
   ![sep](https://github.com/tony-ou/web_QoE_user_study/blob/main/fig/separate_poke2_standardized_plot.png)

