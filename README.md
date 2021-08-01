
# README

## Description

These are source codes for 1video experiment.

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
   cd QoEProject
   ```

3. (Optional) Install all the dependencies:

   This is an optional step for those without `node-modules` folder. If you have downloaded the complete file, all the modules are already in the `node-modules` folder.

   ```shell
   npm install
   ```

4. Start the server on localhost:

   ```shell
   node app.js
   ```

   If you run into any errors regarding modules not found, try removing the "node_modules" folder and go back to step 3.

5. Visit `localhost:3001` on your website, you should see the instruction page.

   If you are running on the uchicago linux machine, visit `linux.cs.uchicago.edu:3001`

   (Optional) If you want to change the port number, in the `app.js` file, edit line 48 to the desired port number.

   After finishing the test, the results will be stored in `./results/`, the file name will be the MTurk ID.

## Running MTurk Survey

1. Login to [Amazon Requester](https://requester.mturk.com/begin_signin) using your Amazon account.

2. Create a new project using their "Survey Link" template.

3. Fill out the survey properties. Here is an example of my settings:
   ![MTurk Settings](https://github.com/sheric98/QoEProject/blob/master/static/MTurk_Settings.png)

4. Click on Design Layout. Click on "Source" in the editor to edit the text.
   Here is an exmaple of my layout:
   ![Design Layout](https://github.com/sheric98/QoEProject/blob/master/static/Design_Layout.png)

   Remember to change the link correspondingly if you changed the port number.

5. Finish and publish a batch.


## About data

1. The raw data collected from the website are .txt files under `./results`, containing info about grades, order of videos, watching and decision time of each grade, and the content of the survey, etc (check `./controllers/start.js` `post_end` function to see what fields are written). 

2. Scripts `./scripts` help you filter, plot, analyze results. Be to sure run these scripts from inside `./scripts` folder, otherwise some paths would be incorrect. First, you should filter out bad results using `./scripts/filter_results.py`. (You can also manually filter results. Run `./scripts/create_csv.py` to put all results into a csv and open it with excel.) Second, you plot MOS + error bar, and obtain a summary log file with `./scripts/get_results.sh`. If results appear weird, you can either revisit filtering step (like increasing filtering threshold) or analyze the results further via `./scripts/Digging.ipynb`. 

3. After you are done with analyzing results, you MUST arhive results with `scripts/move_results_out.sh` because next campaign's results is also stored in `./results`. You will mix them up if you don't archive this campign first. To revisit previous campaigns, run `./scripts/move_results_in.sh`.





