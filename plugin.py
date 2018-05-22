import os
import boto3

def pp(name):
    # pp as in plugin parameter 
    param = os.environ.get('{}_{}'.format('PLUGIN', name.upper()))
    if param:
        return param
    else:
        print '{} is not set'.format(name)
        return None


def env_handler(paramString):
    omap = []
    envSets = paramString.split(',')
    for set in envSets:
        value = set.split('=')[1]
        if set.split('=')[0] == 'EntryPoint':
            value = value.replace(' ', ', ')

        omap.append(
            {
                'ParameterKey': set.split('=')[0],
                'ParameterValue': value
            }
        )

    return omap  


def update_stack(client):
    response = client.update_stack(
        StackName=pp('stackname'),
        UsePreviousTemplate=True,
        Parameters=env_handler(pp('params')),
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
    )
    print response


if __name__ == "__main__":
    # os.environ['AWS_DEFAULT_REGION'] = 'us-east-1' if not pp('region') else pp('region')

    client = boto3.client('cloudformation', region_name='us-east-1')
    update_stack(client)

 
