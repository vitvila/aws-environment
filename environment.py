
# Usage: /home/scripts/environment.py start|stop|restart|create|remove ENV_NAME

import sys
import boto3
import json
import time


# AWS Access Key ID, AWS Secret Key are set in:
# ~/.aws/credentials
# Region is set in:
# ~/.aws/config

#Boto services
client_asg = boto3.client('autoscaling')
client_ec2 = boto3.client('ec2')
client_elb = boto3.client('elb')

#Scripts arguments
args = sys.argv

#Initilizing ASG names from conf file
asg_names = []
for n in range(len(conf['AutoScalingGroups'])):
	asg_names.append(conf['AutoScalingGroups'][n]['AutoScalingGroupName'])

#Initilizing launch configuration names from conf file
launch_conf_names = []
for n in range(len(conf['LaunchConfiguration'])):
	launch_conf_names.append(conf['LaunchConfiguration'][n]['LaunchConfigurationName'])

#Initilizing ELB names from conf file
elb_names = []
for n in range(len(conf['LoadBalancer'])):
	elb_names.append(conf['LoadBalancer'][n]['LoadBalancerName'])




#check_config()
with open('environment.json', 'r') as json_data_file:
    conf = json.load(json_data_file)


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


#=========Conf file check=========

def check_config():
	if os.path.isfile("environment.json") == False:
		print "Please make sure you have a valid configuration file!"
		sys.exit(1)



#=========Start/Stop/Restart=========

def start_asg(asg_names):

	#usage: start_asg(['BE_asg-002'])
	# for loop to start each ASG

	for asg_name in asg_names:

		MinSize="From Conf"
		MaxSize="From Conf"
		DesiredCapacity="From Conf"

		print "Starting ASG: %s" % asg_name
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

	# 'for' loop to stop each ASG
	for asg_name in asg_names:
	    
		#Needed info from config file
		#ASG_NAME_FROM_CONF = []

		#Variables
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


#=========Create==============================================================

def create_launch_conf(launch_conf_names):
	
	#Creating launch configuratoins
	for n in range(len(launch_conf_names)):
		
		image_id =  conf['LaunchConfiguration'][n]['ImageId']
		key_name = conf['LaunchConfiguration'][n]['KeyName']
		instance_type = conf['LaunchConfiguration'][n]['InstanceType']
		associate_ip = conf['LaunchConfiguration'][n]['AssociatePublicIpAddress']
		
		# 'for' loop to initialize list of security groups
		security_groups = []
		for i in range(len(conf['LaunchConfiguration'][n]['SecurityGroups'])):
			security_groups.append(conf['LaunchConfiguration'][n]['SecurityGroups'][i])

		print "Creating Launch Configuration: %s" %  launch_conf_names[n]
		print image_id, key_name, instance_type, associate_ip, security_groups

		'''client_asg.create_launch_configuration(
		LaunchConfigurationName=launch_conf_names[n],
		ImageId=image_id,
		KeyName=key_name,
		SecurityGroups=security_groups,
		InstanceType=instance_type,
		AssociatePublicIpAddress=associate_ip)'''

def create_asg(asg_names):
	
	#Creating ASGs
	for n in range(len(asg_names)):
		launch_conf_name =  conf['AutoScalingGroups'][n]['LaunchConfigurationName']
		min_size = conf['AutoScalingGroups'][n]['MinSize']
		max_size = conf['AutoScalingGroups'][n]['MaxSize']
		desired_size = conf['AutoScalingGroups'][n]['DesiredCapacity']
		
		#'for' loop to initialize list of availability zones
		availability_zones = []
		for i in range(len(conf['AutoScalingGroups'][n]['AvailabilityZones'])):
			availability_zones.append(conf['AutoScalingGroups'][n]['AvailabilityZones'][i])
		#'for' loop to initialize list of load balancer names
		load_balancer_names = []
		for i in range(len(conf['AutoScalingGroups'][n]['LoadBalancerNames'])):
			load_balancer_names.append(conf['AutoScalingGroups'][n]['LoadBalancerNames'][i])
		#'for' loop to initialize list of termination policies
		termination_policies = []
		for i in range(len(conf['AutoScalingGroups'][n]['TerminationPolicies'])):
			termination_policies.append(conf['AutoScalingGroups'][n]['TerminationPolicies'][i])



		print "Creating Auto Scaling Group: %s" %  asg_names[n]
		print asg_names[n], launch_conf_name, min_size, max_size, desired_size, availability_zones, load_balancer_names, termination_policies

		'''client_asg.create_auto_scaling_group(
		AutoScalingGroupName='string',
		LaunchConfigurationName='string',
		MinSize=123,
		MaxSize=123,
		DesiredCapacity=123,
		AvailabilityZones=['string'],
		LoadBalancerNames=['string',],
		TerminationPolicies=['string']
		)'''


def create_elb(elb_names):
			
	#Creating Load Balancers
	for n in range(len(elb_names)):
		# 'for' loop to initialize list of protocols and ports for ELB and Instances attached
		listener_elb_protocol = []
		listener_elb_port = []
		listener_instance_protocol = []
		listener_instance_port = []

		for i in range(len(conf['LoadBalancer'][n]['Listeners'])):
			listener_elb_protocol.append(conf['LoadBalancer'][n]['Listeners'][i]["Protocol"])
			listener_elb_port.append(conf['LoadBalancer'][n]['Listeners'][i]["LoadBalancerPort"])
			listener_instance_protocol.append(conf['LoadBalancer'][n]['Listeners'][i]["InstanceProtocol"])
			listener_instance_port.append(conf['LoadBalancer'][n]['Listeners'][i]["InstancePort"])


		print "Creating Load Balancer: %s" %  elb_names[n]
		print listener_elb_protocol, listener_elb_port, listener_instance_protocol, listener_instance_port

		'''client_elb.create_load_balancer(
	    LoadBalancerName='string',
	    Listeners=[
	        {
	            'Protocol': 'string',
	            'LoadBalancerPort': 123,
	            'InstanceProtocol': 'string',
	            'InstancePort': 123,
	        },
	    ])'''



#=========Remove==============================================================

def remove_asg(asg_names):

	#Removing ASGs
	for asg_name in asg_names:
		print "Removing ASG: %s" % asg_name
		client_asg.delete_auto_scaling_group(AutoScalingGroupName=asg_name)


def remove_launch_config(launch_conf_names):

	#Removing launch configuratoins
	for launch_conf_name in launch_conf_names:
		print "Removing Launch Configuration: %s" % launch_conf_name
		client_asg.delete_launch_configuration(LaunchConfigurationName=launch_conf_name)


def remove_elb(ELB_names):
	
	#Removing ELBs
	for ELB_name in ELB_names:
		print "Removing Load Balancer: %s" % ELB_name
		client_elb.delete_load_balancer(LoadBalancerName=ELB_name)


#=========Tidy_up_configuration=================================================
def config_changes():
	pass

#=========Main==================================================================


check_usage(args)

if args[1] == "start":
	start_asg(asg_names)
elif args[1] == "stop":
	stop_asg(asg_names)
elif args[1] == "restart":
	stop_asg(asg_names)
	start_asg(asg_names)

elif args[1] == "create":
	create_launch_conf(launch_conf_names)
	create_elb(ELB_names)
	create_asg(asg_names)
	
elif args[1] == "remove":
	




