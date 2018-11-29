import boto3
from plugin import pp

parameters = {}

def get_stack_parameters(client, stackName):
    response = client.describe_stacks(StackName=stackname)
    for param in response["Stacks"][0]["Parameters"]:
        parameters[param["ParameterKey"]] = param["ParameterValue"]

    return parameters


