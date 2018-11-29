import boto3
from plugin import pp

def get_stack_parameters(client, stackName):
    parameters = {}
    response = ""
    response = client.describe_stacks(StackName=stackName)
    for param in response["Stacks"][0]["Parameters"]:
        parameters[param["ParameterKey"]] = param["ParameterValue"]

    return parameters


