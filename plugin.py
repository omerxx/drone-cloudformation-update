import os
import boto3
import time
import cloudformation

def pp(name):
    # pp as in plugin parameter 
    param = os.environ.get('{}_{}'.format('PLUGIN', name.upper()))
    if param:
        return param
    else:
        print '{} is not set'.format(name)
        return None


def env_handler(paramString, existingParameters):
    omap = []
    envSets = paramString.split(',')
    for set in envSets:
        key = set.split('=')[0]
        value = set.split('=')[1]
        if key == 'EntryPoint':
            value = value.replace(' ', ', ')

        if key in existingParameters:
            del existingParameters[key]
        
        if value:
            omap.append(
                {
                    'ParameterKey': key,
                    'ParameterValue': value
                }
            )
        else:
            omap.append(
                {
                    'ParameterKey': key,
                    'UsePreviousValue': True
                }
            )

    for pkey in existingParameters.iterkeys():
        omap.append(
            {
                'ParameterKey': pkey,
                'UsePreviousValue': True
            }
        )


    return omap  



def update_stack(client, multistack=False):
    if multistack:
        stackslist = pp('deploylist').split(',')
        targetenv = os.environ.get('DRONE_DEPLOY_TO').split('-')[0]
        for stackname in stackslist:
            existingParameters = cloudformation.get_stack_parameters(client, stackname)
            response = client.update_stack(
                StackName="{}-{}".format(targetenv, stackname),
                UsePreviousTemplate=True,
                Parameters=env_handler(pp('params'), existingParameters),
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
                RollbackConfiguration={
                    'MonitoringTimeInMinutes': 0
                }
            )
            print response

    else:
        existingParameters = cloudformation.get_stack_parameters(client, stackname)
        response = client.update_stack(
            StackName=pp('stackname'),
            UsePreviousTemplate=True,
            Parameters=env_handler(pp('params'), existingParameters),
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
            RollbackConfiguration={
                'MonitoringTimeInMinutes': 0
            }
        )
        print response


def stack_status(client):
    start = time.time()
    timeout = 360 if not pp('timeout') else pp('timeout')
    response = client.describe_stacks(StackName=pp('stackname'))
    status = response["Stacks"][0]["StackStatus"]
    
    while "COMPLETE" not in status and time.time()-start < timeout:
        print '[{}]: {}'.format(time.time()-start, status)
        time.sleep(10)
        response = client.describe_stacks(StackName=pp('stackname'))
        status = response["Stacks"][0]["StackStatus"]
        if "COMPLETE" in status:
            print "Done updating"
            break
    else:
        if status == "UPDATE_IN_PROGRESS":
            response = client.cancel_update_stack(StackName=pp('stackname'))
            print 'Update failed to complete in {} seconds. Aborting and rolling back.'.format(time.time()-start)
        else:
            print 'Check stack {}. Status is {}'.format(pp('stackname'), status)
        
        exit(1)



if __name__ == "__main__":
    region = 'us-east-1' if not pp('region') else pp('region')

    client = boto3.client('cloudformation', region_name=region)
    update_stack(client, pp('deploylist'))

    if not pp('dontwaitfordeploy'):
        time.sleep(10)
        stack_status(client)

 
