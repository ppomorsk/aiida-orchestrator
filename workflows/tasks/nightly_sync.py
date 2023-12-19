import time

import structlog

from orchestrator.targets import Target
from orchestrator.types import State
from orchestrator.workflow import StepList, done, init, step, workflow

import sys
import paramiko
import datetime
import os
import json

logger = structlog.get_logger(__name__)


def get_cluster_data(cluster):
    #account='def-ctetsass_gpu'
    account='def-ctetsass_cpu'
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #ssh.connect('graham.computecanada.ca', username='aiida_ctetsass', password='<password>', key_filename='.ssh/id_aiida_rsa')

    ssh.connect(cluster, username='aiida_ctetsass')


# get cores

    command_string='squeue -A '+account+' -t R,PD --format="%C" -h | paste -s -d+  | bc'

    stdin, stdout, stderr = ssh.exec_command(command_string)
    output=stdout.readlines()

    stdin.close() # close to avoid attribute error with time

    if(output):
        num_cores=int(output[0].strip())
    else: # if no jobs found by squeue
        num_cores=0

# get fairshare
# sshare -n -A def-ctetsass_cpu -U aiida_ctetsass --format "FairShare"
    command_string='sshare -n -A '+account+' -U aiida_ctetsass  --format="FairShare" -h'

    stdin, stdout, stderr = ssh.exec_command(command_string)
    output=stdout.readlines()
    fairshare=float(output[0].strip())

    stdin.close() # close to avoid attribute error with time

    ssh.close()

    return num_cores,fairshare





@step("NSO calls")
def nso_calls() -> State:
    logger.info("Start NSO calls", ran_at=time.time())

    home_dir = os.path.expanduser('~/')
    f=open(home_dir+"aiida-orchestrator/clusterlogs/computers_aiida.json","r")
    computers=f.readlines()
    f.close()
    assert(len(computers)==1)
    computers=json.loads(computers[0])
    for computer in computers:
        cluster=computer["computer"]
        hostname=cluster+".computecanada.ca"
        output=get_cluster_data(hostname)
        ctime=datetime.datetime.now()
        f=open(home_dir+"aiida-orchestrator/clusterlogs/"+cluster+".load.log","a")
        f.write(str(output[0])+","+str(output[1])+","+str(ctime)+"\n")
        f.close()

    logger.info("NSO calls finished", done_at=time.time())


@workflow("Nightly sync", target=Target.SYSTEM)
def task_sync_from() -> StepList:
    return init >> nso_calls >> done
