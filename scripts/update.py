#!/usr/bin/env python
import boto3

organizations_client = boto3.client('organizations')
account_client = boto3.client('account')

def enable_trusted_access():
    trusted_services = organizations_client.list_aws_service_access_for_organization()['EnabledServicePrincipals']
    if not any(x['ServicePrincipal'] == 'account.amazonaws.com' for x in trusted_services):
        organizations_client.enable_aws_service_access(
            ServicePrincipal='account.amazonaws.com'
        )

def get_account_list():
    print("Getting list of accounts in AWS Organizations")
    account_list = []
    management_account_id = organizations_client.describe_organization()['Organization']['MasterAccountId']
    next_page = True
    next_token = ''
    while next_page:
        if next_token:
            response = organizations_client.list_accounts(NextToken="{}".format(next_token))
        else:
            response = organizations_client.list_accounts()

        accounts = response['Accounts']
        
        for account in accounts:
            if account['Status'] == 'ACTIVE' and account['Id'] != management_account_id:
                account_list.append(account['Id'])

        if 'NextToken' in response:
            next_token = response['NextToken'].encode('utf-8')
        else:
            next_page = False
    return account_list


def set_account_contacts(account_id, contacts):
    for contact in contacts:
        print("Updating: {}".format(contact['type']))
        account_client.put_alternate_contact(
            AccountId=account_id,
            AlternateContactType=contact['type'],
            EmailAddress=contact['email'],
            Name=contact['name'],
            PhoneNumber=contact['phone'],
            Title=contact['title']
        )

billing = {
    'type': 'BILLING',
    'name': 'Finance Department',
    'email': 'finance@acme.com',
    'phone': '+31648522680',
    'title': 'Finance Department'
}

security = {
    'type': 'SECURITY',
    'name': 'CISO Office',
    'email': 'security@acme.com',
    'phone': '+316xxxxxxxx',
    'title': 'CISO Office'
}

operations = {
    'type': 'OPERATIONS',
    'name': 'Cloud Platform Team',
    'email': 'operations@acme.com',
    'phone': '+316xxxxxxxx',
    'title': 'Cloud Platform Team'
}

if __name__ == "__main__":
    print("Enabling trusted access for AWS Account Management.")
    enable_trusted_access()

    for account_id in get_account_list():    
        print("Updating alternate contacts for account: {}".format(account_id))
        set_account_contacts(account_id, [billing, security, operations])
