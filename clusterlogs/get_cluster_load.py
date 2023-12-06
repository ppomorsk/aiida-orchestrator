"""

source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon example-orchestrator

"""

import sys
import paramiko
import datetime

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

assert len(sys.argv)==2,"must give cluster name as command line argument"
cluster=sys.argv[1]

# clusters: graham, narval for now
assert cluster=="graham" or cluster=="narval","only graham or narval"

hostname=cluster+".computecanada.ca"
output=get_cluster_data(hostname)
print(output)

ctime=datetime.datetime.now()

f=open(cluster+".load.log","a")
f.write(str(output[0])+","+str(output[1])+","+str(ctime)+"\n")
f.close()


