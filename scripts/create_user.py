import requests
import json

# specify the user group the user to be created will belong to
group_description="si_jobs"
group_description="User Group "+group_description

# get product_id for User Group
x = requests.get('http://127.0.0.1:8080/api/subscriptions/')
y = x.json()

for subscription in y:
    if(subscription["description"]==group_description):
        job_group_id=subscription["subscription_id"]
        break

# want to assign product "User internal" to users so need to find its product it

x = requests.get('http://127.0.0.1:8080/api/products/')
y = x.json()

for product in y:
    if product["name"]=="User internal":
        user_product_id=product["product_id"]


# specify filename with aiida code
filename="/home/ubuntu/aiida-orchestrator/scripts/si.py"

url="http://127.0.0.1:8080/api/processes/create_user"

headers = {"Content-Type": "application/json"}

# need list of dictionaries
data = [
        {"product":user_product_id},
        {"user_group_ids":[job_group_id],"username":filename,"age":112} # age value will be replaced by pk
       ]
# age must be integer





response = requests.post(url, headers=headers , json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())
