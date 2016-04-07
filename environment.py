
# Usage: /home/scripts/environment.py start|stop|restart|create|remove ENV_NAME

import sys
import boto3
import time
import json


# AWS Access Key ID
#aws_key_id=''
# AWS Secret Key
#aws_secret_key=''
# Region
#aws_region=''
#script's arguments
args = sys.argv

#check_config()
with open('environment.json', 'r') as json_data_file:
    conf = json.load(json_data_file)

print conf['AutoScalingGroups'][0]['AutoScalingGroupName']
print ""

#=========Check Usage=========

def check_usage(args):
	arg1 = ["start","stop","restart","create","remove"]
	arg2 = 'ENV_NAME' #Env name from conf file

	if len(args) != 3:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)

	if args[1] not in arg1:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)

	if args[2] not in arg2:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)		


#=========Simple Config Check=========

def check_config():
	if os.path.isfile("environment.conf") == False:
		print "Please make sure you have a valid configuration file!"
		sys.exit(1)



#=========Start/Stop/Restart=========

def start_asg(asg_names):

	#usage: start_asg(['BE_asg-002'])
	# for loop to start each ASG

	for asg_name in asg_names:

		#Needed info from config file
		#asg_names = ['string',]
		MinSize="From Conf"
		MaxSize="From Conf"
		DesiredCapacity="From Conf"

		print "Starting ASG: %s" % asg_name
		client_asg = boto3.client('autoscaling')
		asg_describe = client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

		current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
		current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
		current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
		current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']

		# Checking if instances are still running in asg
		if current_max_size > 0 and current_desired_size > 0:
			print "Seems like instances in ASG: %s are still running" % asg_name
			continue

		#Update Max, Min, Desired amount of instances in ASG
		client_asg.update_auto_scaling_group(
		AutoScalingGroupName=asg_name,
		MinSize=MinSize,
		MaxSize=MaxSize,
		DesiredCapacity=DesiredCapacity)

		time.sleep(60)
		print "Environment is starting."
	
def stop_asg(asg_names):

	#usage: stop_asg(['BE_asg-002'])

	# 'for' loop to stop each ASG
	for asg_name in asg_names:
	    
		#Needed info from config file
		#ASG_NAME_FROM_CONF = []

		#Variables
		client_asg = boto3.client('autoscaling')
		client_ec2 = boto3.client('ec2')
		asg_describe = client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
		current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
		current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
		current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']
		
		#Creating list of instances in asg
		instances = []
		for n in range(len(asg_describe['AutoScalingGroups'][0]['Instances'])):
			instances.append(asg_describe['AutoScalingGroups'][0]['Instances'][n]['InstanceId'])

		print "Stopping ASG: %s" % asg_name

		#Checking if instances already stopped
		if current_max_size == 0 and current_desired_size == 0:
			print "Seems like instances in ASG: %s already stopped" % asg_name
			continue

		#Updating max,min,desired instances to 0 in ASG
		client_asg.update_auto_scaling_group(
		AutoScalingGroupName=asg_name,
		MinSize=0,
		MaxSize=0,
		DesiredCapacity=0)

		#Checking whether all instances in ASG are stoping
		for instance in instances:
			inst_statuse = 'running'
			while inst_statuse == 'running':
				inst_statuse = client_ec2.describe_instances(InstanceIds=[instance])['Reservations'][0]['Instances'][0]['State']['Name']
				print "Instance_id: %s is still running. Waiting for it to be stopped." % instance
				time.sleep( 30 )

		print "Environment successfully stopped."
	

def restart_asg(env_name):
	client_asg = boto3.client('autoscaling')
	asg_describe = client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_NAME_FROM_CONF])
	current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
	current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']

	#Checking if instances already stopped
	if current_max_size == 0 and current_desired_size == 0:
		start_asg()
	else:
		stop_asg()
		start_asg()


#=========Create==============================================================

def create_launch_conf(env_name):

	client_asg = boto3.client('autoscaling')

	response = client_asg.create_launch_configuration(
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

	client_asg = boto3.client('autoscaling')

	response = client_asg.create_auto_scaling_group(
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
	
	client_elb = boto3.client('elb')

	response = client_elb.create_load_balancer(
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

def remove_asg():

	#Initilizing ASG names from conf
	asg_names = []
	for n in range(len(conf['LaunchConfiguration'])):
		 asg_names.append(conf['AutoScalingGroups'][n]['AutoScalingGroupName'])
	print asg_names

	client_asg = boto3.client('autoscaling')

	#Removing ASGs
	for asg_name in asg_names:
		print "Removing ASG: %s" % asg_name
		client_asg.delete_auto_scaling_group(AutoScalingGroupName=asg_name)


def remove_launch_config():
	
	#Initilizing launch_conf_names from conf
	launch_conf_names = []
	for n in range(len(conf['LaunchConfiguration'])):
		 launch_conf_names.append(conf['LaunchConfiguration'][n]['LaunchConfigurationName'])
	print launch_conf_names

	client_asg = boto3.client('autoscaling')

	#Removing launch configuratoins
	for launch_conf_name in launch_conf_names:
		print "Removing Launch Configuration: %s" % launch_conf_name
		client_asg.delete_launch_configuration(LaunchConfigurationName=launch_conf_name)

def remove_elb():
	
	#Initilizing ELB_names list with ELB's from conf
	ELB_names = []
	for n in range(len(conf['LoadBalancer'])):
		 ELB_names.append(conf['LoadBalancer'][n]['LoadBalancerName'])
	print ELB_names

	client_elb = boto3.client('elb')
	
	#Removing ELBs
	for ELB_name in ELB_names:
		print "Removing Load Balancer: %s" % ELB_name
		client_elb.delete_load_balancer(LoadBalancerName=ELB_name)


#=========Tidy_up_configuration=================================================
def config_changes(env_name):
	pass

#=========Main==================================================================

remove_asg()
check_usage(args)

if args[1] == "start":
	start_asg()
elif args[1] == "stop":
	stop_asg()
elif args[1] == "restart":
	restart_asg()

elif args[1] == "create":
	pass
elif args[1] == "remove":
	pass




