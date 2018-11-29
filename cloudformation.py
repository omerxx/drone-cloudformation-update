import boto3
from plugin import pp

def get_stack_parameters(client, stackName):
    parameters = {}
    response = ""
    try:
        response = client.describe_stacks(StackName=stackName)
        for param in response["Stacks"][0]["Parameters"]:
            parameters[param["ParameterKey"]] = param["ParameterValue"]
    except Exception as e:
        print "Error fetching params: {}".format(e)


    return parameters


