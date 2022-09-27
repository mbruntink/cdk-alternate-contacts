import aws_cdk as core
import aws_cdk.assertions as assertions

from alternate_contacts.alternate_contacts_stack import AlternateContactsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in alternate_contacts/alternate_contacts_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AlternateContactsStack(app, "alternate-contacts")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
