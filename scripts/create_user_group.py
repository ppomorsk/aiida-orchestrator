"""

Script to great group of jobs

Name set in job_group_name

"""


import requests

# get product_id for User Group
x = requests.get('http://127.0.0.1:8080/api/products/')
y = x.json()

product_id_list=[]
for product in y:
    if(product["name"]=="User Group"):
        product_id_list.append(product["product_id"])

# should have only one product 
assert(len(product_id_list)==1)

product_id_user_group=product_id_list[0]


# create user group
job_group_name="si_jobs"

url="http://127.0.0.1:8080/api/processes/create_user_group"

headers = {"Content-Type": "application/json"}

# need list of dictionaries
data = [
        {"product":product_id_user_group},
        {"group_name":job_group_name}
       ]


response = requests.post(url, headers=headers , json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())
