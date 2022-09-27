from aws_cdk import (
    Duration,
    Stack,
    aws_lambda,
    aws_iam,
    aws_events,
    aws_events_targets
)
from constructs import Construct
class AlternateContactsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        update_contacts_function = aws_lambda.Function(
            scope=self,
            id="UpdateContactFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset('lambda/update-contacts'),
            memory_size=128,
            environment={
                "BILLING_CONTACT_NAME": "Finance",
                "BILLING_EMAIL": "finance@acme.com",
                "BILLING_CONTACT_PHONE": "+316xxxxxxxx",
                "BILLING_CONTACT_TITLE": "Finance",
                "SECURITY_CONTACT_NAME": "CISO Office",
                "SECURITY_EMAIL": "security@acme.com",
                "SECURITY_CONTACT_PHONE": "+316xxxxxxxx",
                "SECURITY_CONTACT_TITLE": "CISO Office",
                "OPERATIONS_CONTACT_NAME": "Cloud Platform Team",
                "OPERATIONS_EMAIL": "operations@acme.com",
                "OPERATIONS_CONTACT_PHONE": "+316xxxxxxxxxx",
                "OPERATIONS_CONTACT_TITLE": "Cloud Platform Team",
            },
            timeout=Duration.minutes(1),
            handler='app.lambda_handler',
        )      
      
        # Allow the function to update account contact information
        update_contacts_function.role.add_to_principal_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    'account:PutAlternateContact'
                ],
                resources=[
                    "arn:aws:account::{}:account/*".format(self.account)
                ],
            )
        )
        
        # Add event to trigger Lambda
        organizations_rule = aws_events.Rule(
            scope=self, 
            id="OrganizationsRule",
            event_pattern=aws_events.EventPattern(
                source=["aws.organizations"],
                detail=dict(
                    eventName=["CreateAccountResult"],
                    eventSource=["organizations.amazonaws.com"],
                    serviceEventDetails=dict(
                        createAccountStatus=dict(
                            state=['SUCCEEDED']
                        )
                    )
                )
            )
        )   
        organizations_rule.add_target(target=aws_events_targets.LambdaFunction(update_contacts_function))

        control_tower_rule = aws_events.Rule(
            scope=self, 
            id="ControlTowerRule",
            event_pattern=aws_events.EventPattern(
                source=["aws.controltower"],
                detail=dict(
                    eventName=["CreateManagedAccount"],
                    eventSource=["controltower.amazonaws.com"],
                    serviceEventDetails=dict(
                        createAccountStatus=dict(
                            state=['SUCCEEDED']
                        )
                    )
                )
            )
        )   
        control_tower_rule.add_target(target=aws_events_targets.LambdaFunction(update_contacts_function))