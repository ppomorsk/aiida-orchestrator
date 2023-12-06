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

Need to have:

verdi computer graham and narval set up as computers (under those exact names)

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

In the clusterlogs there are scripts which should be run periodically to log the load on the clusters,
which is stored in log files, separate for each cluster (should use database for this in the future).

Currently the monitoring scripts are run by hand, but they could be modified to run as cron jobs, or run
inside the orchestrator itself as a periodically executed task.

The file computers_aiida.json contains a list of active computers to be used by the the orchestrator to 
launch AiiDA jobs.

For details of how the monitoring data is used see:

~/aiida-orchestrator/workflows/user/create_user.py 


