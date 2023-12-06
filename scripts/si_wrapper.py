"""
Simple wrapper to run AiiDA job without orchestrator

"""


from subprocess import PIPE, run

file_name ="/home/ubuntu/aiida-orchestrator/scripts/si.py" 

computerselect="narval"

cmd='python3 '+file_name+" "+computerselect
print("cmd is: ", cmd)
cmd=cmd.split()

result = run(cmd, stdout=PIPE, stderr=PIPE, text=True)

#print(result.returncode, result.stdout, result.stderr)
#print(type(result.stdout))


s=result.stdout
s=s[s.find("uuid")+6:]
uuid = s[:s.find(" ")]
s=s[s.find("pk")+4:]
pk=s[:s.find(")")]

print("uuid=",uuid,"pk=",pk)
