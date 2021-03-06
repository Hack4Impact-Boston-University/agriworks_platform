# Agriworks Backend

## Run & Develop
0. Install Docker https://www.docker.com/products/docker-desktop
1. Clone this repo and the portal (frontend) repo   https://github.com/Hack4Impact-Boston-University/agriworks_portal within a parent directory.
2. Request the credentials file from a fellow developer and place it in the platform root directory.
3. Run the command `docker-compose up` in either repo. 

## Build & Deploy

0. Push to the master branch in either repository. 

## Old Develop Instructions:
To run the application, first follow the steps below to setup the project on your local machine.

0. Verify that you have python3 installed on your machine. If not, install it.
1. Clone this project to your local machine.
2. Create a virtual environment for this project using `python3 -m venv env` inside the directory
3. Activate the virtual environment using the command `source env/bin/activate`
4. Install our current dependencies using the command `pip install -r requirements.txt`
5. (Unix) Navigate to the directory of your project and run the command `chmod u+x start.sh`. 
   (Windows) Execute `setEnvVars.bat`. 

6.(Unix) Execute `./start.sh` to start the application. 
   (Windows) Execute the command `flask run` to start the application. 

Navigate to http://localhost:4000/api/admin/. If you see a JSON response stating that Agriworks is running, you have successfully setup the project correctly.
