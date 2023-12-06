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

## Use GUI
Now point your browser to `http://localhost:3000/` and have a look around.
You can use the `New Process` button to create subscription on the defined
products.
