# 
AiiDA Orchestrator

## Preliminaries - set up VM

Ubuntu

```shell
sudo apt-get update
sudo apt-get upgrade
sudo reboot
sudo apt-get dist-upgrade
sudo reboot
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
sudo apt-get install --yes postgresql git virtualenvwrapper nodejs
sudo apt  install gh
```

## AiiDA setup

Need to have graham and narval set up as computers (under those exact names)

Need to have VASP codes set up in aiida under vasp@graham and vasp@narval.

Need to have ssh access under aiida_ctetsass account to graham and narval.

## Create database

```shell
chmod go+rX /home/ubuntu/
# set password to: nwa
sudo -u postgres createuser -sP nwa
sudo -u postgres createdb orchestrator-core -O nwa
```

## Install orchestrator

```shell
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv --python python3.10 example-orchestrator
# older version as newer breaks gui
pip install orchestrator-core==1.1.0
```

To use this environment later, run:

```shell
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon example-orchestrator
```


## Install aiida-orchestrator

```shell
git clone git@github.com:ppomorsk/aiida-orchestrator.git
cd aiida-orchestrator
# when running git for first time
git config --local user.email "ppomorsk@sharcnet.ca"
git config --local user.name "Pawel Pomorski"

PYTHONPATH=. python main.py db init
cp examples/2023-12-05_*  migrations/versions/schema/
PYTHONPATH=. python main.py db upgrade heads
```


## Start orchestrator

```shell
# if environment not active yet, run
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon example-orchestrator
# then start the app
cd aiida-orchestrator
uvicorn --host 127.0.0.1 --port 8080 main:app
```

## Install GUI

```shell
git clone https://github.com/workfloworchestrator/orchestrator-core-gui.git
cd orchestrator-core-gui/
sudo npm install --global yarn
sudo npm install --global --save-dev npm-run-all
yarn install

cp .env.local.example .env.local
```

Edit .env.local to have

```shell
# change the existing REACT_APP_BACKEND_URL variable value into:
REACT_APP_BACKEND_URL=http://127.0.0.1:3000
# and add the following:
DANGEROUSLY_DISABLE_HOST_CHECK=true
```

After editing, run:

```shell
(cd src && ln -s custom-example custom)
```

## Run GUI

```shell
cd orchestrator-core-gui
source .env.local
yarn start
```

## Open SSH tunnels

To view the GUI in local browser, run on your local machine, in two terminal windows:


```shell
ssh -L 8080:localhost:8080  ubuntu@206.12.89.248
ssh -L 3000:localhost:3000  ubuntu@206.12.89.248
```

Change 206.12.89.248 to actual IP of your VM.

## Interface with the app

Documentation:

http://127.0.0.1:8080/api/docs

Also can try:

http://127.0.0.1:8080/api/workflows/

http://127.0.0.1:8080/api/subscriptions/all

http://127.0.0.1:8080/api/processes/

http://127.0.0.1:8080/api/products/

GUI:

http://127.0.0.1:3000

If GUI gives blank page, try

http://127.0.0.1:3000/subscriptions

You can use the `New Process` button to create subscription on the defined
products.


## Using the command line

The GUI can be used to launch processes, i.e. create user groups (job groups) and users (jobs).
However, filling out the forms by hand is only useful for basic testing.

For submitting a larger number of jobs, one needs command line tools.  
That is provided in scripts directory.

First, need to create at least one user group (job group) that every job needs to have.

Do this by running:

python create_user_group.py

Job group name can be changed in the script as needed.

Then submit job by running:

python create_user.py

The file name of the AiiDA script to be launched needs to be specified.

The script needs to have a specific format, as it has to accept the cluster name as argument.

Take a look at si.py for an example.

Finaly, si_wrapper.py can launch this AiiDA job outside of the orchestrator.

## Monitoring the clusters

The file computers_aiida.json contains a list of active computers to be used by the the orchestrator to
launch AiiDA jobs.  It is assumbed that it is possible to connect these to ssh and launch
AiiDA processes.

In the clusterlogs there are scripts which can be executed  to log the load on the clusters,
which is stored in log files, separate for each cluster (should use database for this in the future).

The monitoring scripts can be run by hand, or they could be modified to run as cron jobs,

These are for testing only, as proper monitoring should be a task in the orchestrator:

~/aiida-orchestrator/workflows/tasks/nightly_sync.py

This task will be available in the task launching interface of orchestrator GUI.

However, it should be run as a scheduled task, as described below.

For details of how the monitoring data is used see:

~/aiida-orchestrator/workflows/user/create_user.py 

## Scheduling tasks

Schedules for running tasks can be defined in

~/aiida-orchestrator/schedules

This creates schedules in addition to those defined in orchestrator itself.

The schedules currently set can be listed with:

python main.py scheduler show-schedule

Any one of these can be forced to run immediately with:

PYTHONPATH=. python main.py scheduler force run_nightly_monitoring

To start running the scheduler, execute and keep running

PYTHONPATH=. python main.py scheduler run

## Developing the code

If any changes are made to the migration files, then the database needs to be rebuilt.

Doing this is also useful if the orchestrator or GUI gets into disfunctional state.

```shell
sudo -u postgres psql

DROP DATABASE "orchestrator-core";

exit

sudo -u postgres createdb orchestrator-core -O nwa

# get fresh git checkout if orchestrator code changed

rm -rf aiida-orchestrator
git clone git@github.com:ppomorsk/aiida-orchestrator.git
cd aiida-orchestrator

source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon example-orchestrator

# remove migrations directory if it exists

rm -rf migrations 

PYTHONPATH=. python main.py db init
cp examples/2023*.py  migrations/versions/schema/
PYTHONPATH=. python main.py db upgrade heads

```


