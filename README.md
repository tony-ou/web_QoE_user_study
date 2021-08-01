
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

4. Start the server on localhost:

   ```shell
   node app.js [Optionally specify which port to run server; defaults to 3001 if not specified]
   ```

   If you run into any errors regarding modules not found, try removing the "node_modules" folder and go back to step 3.

5. Visit `localhost:3001` on your website, you should see the instruction page.

   If you are running on the uchicago farewell cluster, visit `farewell.cs.uchicago.edu:3001`

   After finishing the test, the results will be stored in `./results/`, the file name will be the MTurk ID.

## Prepare for mturk campaign

1. First create test videos. (Check [this](https://github.com/tony-ou/web_QoE_video_creation/) repo). 

2. We need to host videos online for users to watch them. A simple solution is to put it under `./campaign/{video folder name}` and so the final video_url will be like ` "https://raw.githubusercontent.com/tony-ou/web_QoE_user_study/main/campaign/" + vid_folder + "/1.mp4"`. But if there're too many vids, you may reach github repo's limit. 

Other solutions are Google Cloud Storage or Amazon S3. But you will need to modify scripts in `/scripts/` and `controllers/app.js` because some of them reference `./campaign/` folder.

3. Update `vid_folder` variable and `video_order` variable in `start.js`. Video order is usually randomized for each user so we don't get biased results. Sometime, you may want to specify a video's location if that is a reference video. (e.g. a video with fastest page load such that user must give it highest rating, otherwise we reject the user. In this case we can fix it to the last position.)


## About data

1. The raw data collected from the website are .txt files under `./results`, containing info about grades, order of videos, watching and decision time of each grade, and the content of the survey, etc (check `./controllers/start.js` `post_end` function to see what fields are written). 

2. Scripts `./scripts` help you filter, plot, analyze results. Be to sure run these scripts from inside `./scripts` folder, otherwise some paths would be incorrect. First, you should filter out bad results using `./scripts/filter_results.py`. (You can also manually filter results. Run `./scripts/create_csv.py` to put all results into a csv and open it with excel.) Bad results will be moved to `./rejected_results`. Second, you plot MOS + error bar, and obtain a summary log file with `./scripts/get_results.sh`. If results appear weird, you can either revisit filtering step (like increasing filtering threshold) or analyze the results further via `./scripts/Digging.ipynb`. 

3. After you are done with analyzing results, you **MUST** archive results with `scripts/move_results_out.sh` because next campaign's results is also stored in `./results`. You will mix them up if you don't archive this campaign first. To revisit previous campaigns, run `./scripts/move_results_in.sh`. The results are archived to `./old_results`





