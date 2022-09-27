import boto3
import os

account_client = boto3.client('account')

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

def lambda_handler(event, context):

    billing_contact = {
        'type': 'BILLING',
        'name': os.environ["BILLING_CONTACT_NAME"],
        'email': os.environ["BILLING_EMAIL"],
        'phone': os.environ["BILLING_CONTACT_PHONE"],
        'title': os.environ["BILLING_CONTACT_TITLE"]
    }

    security_contact = {
        'type': 'SECURITY',
        'name': os.environ["SECURITY_CONTACT_NAME"],
        'email': os.environ["SECURITY_EMAIL"],
        'phone': os.environ["SECURITY_CONTACT_PHONE"],
        'title': os.environ["SECURITY_CONTACT_TITLE"]
    }
    
    operations_contact = {
        'type': 'OPERATIONS',
        'name': os.environ["OPERATIONS_CONTACT_NAME"],
        'email': os.environ["OPERATIONS_EMAIL"],
        'phone': os.environ["OPERATIONS_CONTACT_PHONE"],
        'title': os.environ["OPERATIONS_CONTACT_TITLE"]
    }
    
    if event["detail-type"] == "AWS Service Event via CloudTrail":
        detail = event["detail"]
        if detail.get("serviceEventDetails",{}).get("createAccountStatus",{}).get('state') == "SUCCEEDED":
            account_id = detail['serviceEventDetails']['createAccountStatus']['accountId']
        if detail.get("serviceEventDetails",{}).get("createManagedAccountStatus",{}).get('state') == "SUCCEEDED":
            account_id = detail['serviceEventDetails']['createManagedAccountStatus']['account']['accountId']

        print("Updating alternate contacts for: {}".format(account_id))
        set_account_contacts(account_id, [security_contact, billing_contact, operations_contact])

    # Event Example:
    # {
    #     'version': '0', 
    #     'id': '152031b5-647f-4e9a-ebc9-9be32bd221ee', 
    #     'detail-type': 'AWS Service Event via CloudTrail', 
    #     'source': 'aws.organizations', 
    #     'account': 'xxxxxxxxx', 
    #     'time': '2022-09-27T08:29:47Z', 
    #     'region': 'us-east-1', 
    #     'resources': [], 
    #     'detail': {
    #         'eventVersion': '1.08', 
    #         'userIdentity': {
    #             'accountId': 'xxxxxxxxxxxxx', 
    #             'invokedBy': 'AWS Internal'
    #         },
    #         'eventTime': '2022-09-27T08:29:47Z',
    #         'eventSource': 'organizations.amazonaws.com', 
    #         'eventName': 'CreateAccountResult', 
    #         'awsRegion': 'us-east-1', 
    #         'sourceIPAddress': 'AWS Internal', 
    #         'userAgent': 'AWS Internal', 
    #         'requestParameters': None, 
    #         'responseElements': None, 
    #         'eventID': '64c8e863-76f4-4aad-9c16-b8b0a9a97203', 
    #         'readOnly': False, 'eventType': 'AwsServiceEvent',
    #         'managementEvent': True,
    #         'recipientAccountId': 'xxxxxxxxxxxxxx', 
    #         'serviceEventDetails': {
    #             'createAccountStatus': {
    #                 'id': 'car-89bc31e03e3e11edb27f0e74a065c757',
    #                 'state': 'SUCCEEDED',
    #                 'accountName': '****',
    #                 'accountId': 'xxxxxxxxxxxxx',
    #                 'requestedTimestamp': 'Sep 27, 2022 8:29:44 AM',
    #                 'completedTimestamp': 'Sep 27, 2022 8:29:47 AM'
    #             }
    #         }, 
    #         'eventCategory': 'Management'
    #     }
    # }
