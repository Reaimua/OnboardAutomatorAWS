import boto3
import pandas as pd

def create_user_in_group_with_role (user_name, department, role_name, employee_type):
    iam_client = boto3.client('iam')

    #Check employee type and add prefix
    if employee_type == "Vendor":
        user_name ='ven-'+ user_name
    elif employee_type == "Temporary":
        user_name ='t-'+ user_name
    #Create the IAM user
    iam_client.create_user(UserName=user_name)

    #Add User to their Department 
    iam_client.add_user_to_group(UserName= user_name, GroupName= department)

    #Add a Managerial or Employee Role to User
    if role_name == "Manager":
        iam_client.attach_user_to_policy(UserName=user_name, PolicyArn= f'arn:aws:iam::aws:policy/{role_name}')
    else: 
        iam_client.attach_user_to_policy(UserName=user_name, PolicyArn= f'arn:aws:iam::aws:policy/{role_name}')


def create_users_from_excel(excel_file):
    data = pd.read_excel(excel_file)

    for index, data in data.iterrows():
        first_name = data['First Name']
        last_name = data['Last Name']
        department = data['Department']
        position =  data['Position']
        username = data['Username']
        email = data ['Email']
        employeeType= data ['Employee Type']

        create_user_in_group_with_role (username, department, position, employeeType)

excel_file = "/Users/ryansmac/Documents/GitHub/OnboardAutomatorAWS/NewUserTemplate.xlsx"
create_users_from_excel(excel_file)

