from typing import List, Optional
from uuid import uuid4

from orchestrator.db.models import ProductTable, SubscriptionTable
from orchestrator.forms import FormPage
from orchestrator.forms.validators import Choice, choice_list
from orchestrator.targets import Target
from orchestrator.types import FormGenerator, State, SubscriptionLifecycle, UUIDstr
from orchestrator.workflow import done, init, step, workflow
from orchestrator.workflows.steps import resync, set_status, store_process_subscription
from orchestrator.workflows.utils import wrap_create_initial_input_form

from products.product_types.user import UserInactive, UserProvisioning
from products.product_types.user_group import UserGroup

from subprocess import PIPE, run

def user_group_selector() -> list:
    user_group_subscriptions = {}
    for user_group_id, user_group_description in (
        SubscriptionTable.query.join(ProductTable)
        .filter(
            ProductTable.product_type == "UserGroup",
            SubscriptionTable.status == "active",
        )
        .with_entities(SubscriptionTable.subscription_id, SubscriptionTable.description)
        .all()
    ):
        user_group_subscriptions[str(user_group_id)] = user_group_description

    return choice_list(
        Choice("UserGroupEnum", zip(user_group_subscriptions.keys(), user_group_subscriptions.items())),  # type:ignore
        min_items=1,
        max_items=1,
    )


def initial_input_form_generator(product_name: str) -> FormGenerator:
    # def initial_input_form_generator(product: UUIDstr, product_name: str) -> FormGenerator:

    # _product = ProductTable.get_product_by_id(product)
    # affiliation = _product.fixed_input_value('affiliation')

    class CreateUserForm(FormPage):
        class Config:
            title = product_name

        username: str
        age: Optional[int]
        user_group_ids: user_group_selector()  # type:ignore

    user_input = yield CreateUserForm

    return user_input.dict()


def _provision_in_user_management_system(username: str, age: int) -> int:

    return abs(hash(username))


@step("Create subscription")
def create_subscription(product: UUIDstr) -> State:
    subscription = UserInactive.from_product_id(product, str(uuid4()))

    return {"subscription": subscription, "subscription_id": subscription.subscription_id}


@step("Initialize subscription")
def initialize_subscription(subscription: UserInactive, username: str, age: int, user_group_ids: List[str]) -> State:
    subscription.user.username = username
    subscription.user.age = age
    subscription.user.group = UserGroup.from_subscription(user_group_ids[0]).user_group
    subscription.description = (
        f"User {username} from group {subscription.user.group.group_name} ({subscription.affiliation})"
    )
    subscription = UserProvisioning.from_other_lifecycle(subscription, SubscriptionLifecycle.PROVISIONING)

    import json

    f=open("/home/ubuntu/aiida-orchestrator/clusterlogs/computers_aiida.json","r")
    g=f.readlines()
    f.close()

    computers=json.loads(g[0])
    computer_list=[]
    for d in computers:
        computer_list.append(d["computer"])


    fairshare_list=[]
    for cluster in computer_list:

        f=open("/home/ubuntu/aiida-orchestrator/clusterlogs/"+cluster+".load.log","r")
        g=f.readlines()
        f.close()
        last=g[-1].split(",")
        fairshare_list.append(last[1])

    maxfairshare=fairshare_list.index(max(fairshare_list))
    computerselect=computer_list[maxfairshare]

    cmd='python3 '+username+" "+computerselect

    cmd=cmd.split()

    result = run(cmd, stdout=PIPE, stderr=PIPE, text=True)

    s=result.stdout
    s=s[s.find("uuid")+6:]
    uuid_val = s[:s.find(" ")]
    s=s[s.find("pk")+4:]
    pk_val=s[:s.find(")")]

    subscription.user.age = int(pk_val)

    return {"subscription": subscription}


@step("Provision user")
def provision_user(subscription: UserProvisioning, username: str, age: int) -> State:
    user_id = _provision_in_user_management_system(username, age)
    subscription.user.user_id = user_id

    return {"subscription": subscription}


@workflow(
    "Create user",
    initial_input_form=wrap_create_initial_input_form(initial_input_form_generator),
    target=Target.CREATE,
)
def create_user():

    return (
        init
        >> create_subscription
        >> store_process_subscription(Target.CREATE)
        >> initialize_subscription
        >> provision_user
        >> set_status(SubscriptionLifecycle.ACTIVE)
        >> resync
        >> done
    )
