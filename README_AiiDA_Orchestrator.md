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


## Start orchestraor

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
