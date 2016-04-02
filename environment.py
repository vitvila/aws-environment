# Usage: /home/scripts/environment.py start|stop|restart|create|remove ENV_NAME

import sys
import boto3


#Variables

# AWS Access Key ID
aws_key_id=''
# AWS Secret Key
aws_secret_key=''
# Region
aws_region=''
#script's arguments
args = sys.argv




#=========Check Usage=========

def check_usage(args):
	arg1 = ["start","stop","restart","create","remove"]
	arg2 = ENV_NAME #Env name from conf file

	if len(args) != 3:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)

	if args[1] not in arg1:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)

	if args[2] not in arg2:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)		


#=========Check Config=========

def check_config():
	if os.path.isfile("environment.conf") == False:
		print "Please make sure you have a valid configuration file!"
		sys.exit(1)



#=========Start/Stop/Restart=========

def start_asg(env_name):
    
    #Needed info from config file

    #ASG_NAME_FROM_CONF = []
    #MinSize=integer
    #MaxSize=integer

    client = boto3.client('autoscaling')

    asg_describe = client.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_NAME_FROM_CONF])
    if asg_describe{'AutoScalingGroups'[{"MaxSize"}]} != 0:
        print "Seems like instances in ASG: %s are still running" % ASG_NAME_FROM_CONF
        sys.exit(1)

	response = client.update_auto_scaling_group(
    AutoScalingGroupName='string',
    LaunchConfigurationName='string',
    MinSize=123,
    MaxSize=123,
    DesiredCapacity=123,
    DefaultCooldown=123,
    AvailabilityZones=[
        'string',
    ],
    HealthCheckType='string',
    HealthCheckGracePeriod=123,
    PlacementGroup='string',
    VPCZoneIdentifier='string',
    TerminationPolicies=[
        'string',
    ],
    NewInstancesProtectedFromScaleIn=True|False
)
	


def stop_asg(env_name):
	
    #Needed info from config file
    #ASG_NAME_FROM_CONF = []

	client = boto3.client('autoscaling')

	response = client.update_auto_scaling_group(
    AutoScalingGroupName='string',
    LaunchConfigurationName='string',
    MinSize=123,
    MaxSize=123,
    DesiredCapacity=123,
    DefaultCooldown=123,
    AvailabilityZones=[
        'string',
    ],
    HealthCheckType='string',
    HealthCheckGracePeriod=123,
    PlacementGroup='string',
    VPCZoneIdentifier='string',
    TerminationPolicies=[
        'string',
    ],
    NewInstancesProtectedFromScaleIn=True|False
	)
	

def restart_asg(env_name):
	if check_status(InstanceId) == 'Running':
	 	stop_asg()
	 	start_asg()
	else:
	 	start_asg()






#=========Create==============================================================

def create_launch_conf(env_name):

	client = boto3.client('autoscaling')

	response = client.create_launch_configuration(
    LaunchConfigurationName='string',
    ImageId='string',
    KeyName='string',
    SecurityGroups=[
        'string',
    ],
    ClassicLinkVPCId='string',
    ClassicLinkVPCSecurityGroups=[
        'string',
    ],
    UserData='string',
    InstanceId='string',
    InstanceType='string',
    KernelId='string',
    RamdiskId='string',
    BlockDeviceMappings=[
        {
            'VirtualName': 'string',
            'DeviceName': 'string',
            'Ebs': {
                'SnapshotId': 'string',
                'VolumeSize': 123,
                'VolumeType': 'string',
                'DeleteOnTermination': True|False,
                'Iops': 123,
                'Encrypted': True|False
            },
            'NoDevice': True|False
        },
    ],
    InstanceMonitoring={
        'Enabled': True|False
    },
    SpotPrice='string',
    IamInstanceProfile='string',
    EbsOptimized=True|False,
    AssociatePublicIpAddress=True|False,
    PlacementTenancy='string'
	)

def create_asg(env_name):
	
	# create_launch_conf()

	client = boto3.client('autoscaling')

	response = client.create_auto_scaling_group(
    AutoScalingGroupName='string',
    LaunchConfigurationName='string',
    InstanceId='string',
    MinSize=123,
    MaxSize=123,
    DesiredCapacity=123,
    DefaultCooldown=123,
    AvailabilityZones=[
        'string',
    ],
    LoadBalancerNames=[
        'string',
    ],
    HealthCheckType='string',
    HealthCheckGracePeriod=123,
    PlacementGroup='string',
    VPCZoneIdentifier='string',
    TerminationPolicies=[
        'string',
    ],
    NewInstancesProtectedFromScaleIn=True|False,
    Tags=[
        {
            'ResourceId': 'string',
            'ResourceType': 'string',
            'Key': 'string',
            'Value': 'string',
            'PropagateAtLaunch': True|False
        },
    ]
	)


def create_elb(env_name):
	
	client = boto3.client('elb')

	response = client.create_load_balancer(
    LoadBalancerName='string',
    Listeners=[
        {
            'Protocol': 'string',
            'LoadBalancerPort': 123,
            'InstanceProtocol': 'string',
            'InstancePort': 123,
            'SSLCertificateId': 'string'
        },
    ],
    AvailabilityZones=[
        'string',
    ],
    Subnets=[
        'string',
    ],
    SecurityGroups=[
        'string',
    ],
    Scheme='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ]
    )






#=========Remove==============================================================

def remove_asg(env_name):

	client = boto3.client('autoscaling')

	response = client.delete_auto_scaling_group(
    AutoScalingGroupName='string',
    ForceDelete=True|False
    )


def remove_launch_config(env_name):

	client = boto3.client('autoscaling')

	response = client.delete_launch_configuration(
    LaunchConfigurationName='string'
    )

def remove_elb(env_name):

	client = boto3.client('autoscaling')
	
	response = client.delete_load_balancer(
    LoadBalancerName='string'
    )






#=========Tidy_up_configuration=================================================
def config_changes(env_name):




#=========Main==================================================================

if args[1] == "start":
	start_asg("env_name")

elif args[1] == "stop":
	stop_asg()

elif args[1] == "restart":
	stop_asg("env_name")
	start_asg("env_name")

elif args[1] == "create":
	pass
elif args[1] == "remove":
	pass




# AWS random code. Archive=========================================================
"""
conn_to_region = boto.ec2.connect_to_region("us-west-2", aws_access_key_id='<aws access key>', aws_secret_access_key='<aws secret key>')

#Stopping/Terminating
ec2.instances.filter(InstanceIds=ids).stop()
ec2.instances.filter(InstanceIds=ids).terminate()

# ASG
conn = boto.connect_autoscale()
config = LaunchConfiguration(name='foo', image_id='ami-abcd1234', key_name='foo.pem')
conn.create_launch_configuration(config)


# Botto3 examples
In [19]: rc = ec2.resource.create_instances(
    ImageId = ec2.getami('NetBSD*64*6.1.5*'),
    MinCount = 1,
    MaxCount = 1,
    KeyName = 'mysshpemkey',
    InstanceType = 'm3.medium',
    PrivateIpAddress = '10.10.0.1',
    SubnetId = ec2.get_id_from_nametag('subnets', 'examplesubnet')
)
In [20]: print(rc[0].id)
i-b1774f1b

