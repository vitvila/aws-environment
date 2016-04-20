
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


#Handling exceptions if 'environment.json' file is not valid.
try:
	with open('environment.json', 'r') as json_data_file:
		conf = json.load(json_data_file)
except IOError: # If conf file is not found
	print "Please make sure you have a valid 'environment.json' configuration file."
	sys.exit(1)
except ValueError: # If json syntax is incorrect in conf file
	print "Please check syntax of 'environment.json' configuration file."
	sys.exit(1)


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


#=========Check Usage=========

def check_usage(args):
	arg1 = ["start","stop","restart","create","remove"]
	arg2 = 'ENV_NAME' #Env names from 

	if len(args) != 3:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)

	if args[1] not in arg1:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)

	if args[2] not in arg2:
		print "Wrong usage!!! Please use: environment.py start|stop|restart|create|remove ENV_NAME"
		sys.exit(1)		


#=========Start/Stop/Restart=========

def start_asg(asg_names):

	# 'for' loop to update max,min,desired in each ASG from conf file.
	for n in range(len(asg_names)):
		try:
			#Conf file settings of asg
			min_size = conf['AutoScalingGroups'][n]['MinSize']
			max_size = conf['AutoScalingGroups'][n]['MaxSize']
			desired_size = conf['AutoScalingGroups'][n]['DesiredCapacity']
			
			#Checking current aws asg settings
			asg_describe = client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_names[n]])
			current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
			current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
			current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']
		
		except KeyError, e: # If variable missed from conf file
			print "Please check your 'environment.json' config file."
			print "ASG: %s" % asg_names[n]
			print "The problem: %s." % e
			sys.exit(1)
		
		except IndexError: #If wrong name of asg in conf file
			print "Please make sure you're using correct name of asg %s" % asg_names[n]
			sys.exit(1)
		
		finally:
			json_data_file.close()

		#Checking if instances are still running in asg
		if current_max_size > 0 and current_desired_size > 0:
			print "Seems like instances in ASG: %s are still running. Max and Desired amount > 0" % asg_name[n]
			continue

		print "Starting %s instance(s) in ASG: %s" % (desired_size, asg_names[n])

		#Update Max, Min, Desired amount of instances in ASG to start environment.
		client_asg.update_auto_scaling_group(
		AutoScalingGroupName=asg_names[n],
		MinSize=min_size,
		MaxSize=max_size,
		DesiredCapacity=desired_size)

	time.sleep(50)
	print "Environment is started."

def stop_asg(asg_names):

	# 'for' loop to stop instances in each ASG
	for n in range(len(asg_names)):
		try:
			#Checking current aws asg settings
			asg_describe = client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_names[n]])
			current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
			current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
			current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']

			#Creating list of instance IDs in asg
			instances = []
			for i in range(len(asg_describe['AutoScalingGroups'][0]['Instances'])):
				instances.append(asg_describe['AutoScalingGroups'][0]['Instances'][i]['InstanceId'])
		
		except IndexError: # If no ASG with this name in aws
			print "Please check you Auto Scaling group %s" % asg_names[n]
			sys.exit(1)

		print "Stopping %s instance(s) in ASG: %s" % (len(instances), asg_names[n])

		#Checking if instances already stopped
		if current_max_size == 0 and current_desired_size == 0:
			print "Seems like instances in ASG: %s already stopped" % asg_names[n]
			continue

		#Updating max,min,desired instances to 0 to stop all instances in asg
		client_asg.update_auto_scaling_group(
		AutoScalingGroupName=asg_names[n],
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
		print "Instances in %s successfully stopped." % asg_names[n]



#=========Create==============================================================

def create_launch_conf(launch_conf_names):
	
	#Creating launch configuratoins
	for n in range(len(launch_conf_names)):
		try:
			#Parsing variables from json conf file
			image_id =  conf['LaunchConfiguration'][n]['ImageId']
			key_name = conf['LaunchConfiguration'][n]['KeyName']
			instance_type = conf['LaunchConfiguration'][n]['InstanceType']
			associate_ip = conf['LaunchConfiguration'][n]['AssociatePublicIpAddress']
			
			# 'for' loop to initialize list of security groups
			security_groups = []
			for i in range(len(conf['LaunchConfiguration'][n]['SecurityGroups'])):
				security_groups.append(conf['LaunchConfiguration'][n]['SecurityGroups'][i])

		except KeyError, e: # If variable missed from conf file
			print "Please check your 'environment.json' config file."
			print "Launch Configuration: %s" % launch_conf_names[n]
			print "The problem: %s." % e
			sys.exit(1)

		print "Creating Launch Configuration: %s" %  launch_conf_names[n]
		print image_id, key_name, instance_type, associate_ip, security_groups
		
		client_asg.create_launch_configuration(
		LaunchConfigurationName=launch_conf_names[n],
		ImageId=image_id,
		KeyName=key_name,
		SecurityGroups=security_groups,
		InstanceType=instance_type,
		AssociatePublicIpAddress=associate_ip)

def create_asg(asg_names):
	
	#Creating ASGs
	for n in range(len(asg_names)):
		
		try:
			#Parsing variables from json conf file
			launch_conf_name =  conf['AutoScalingGroups'][n]['LaunchConfigurationName']
			min_size = conf['AutoScalingGroups'][n]['MinSize']
			max_size = conf['AutoScalingGroups'][n]['MaxSize']
			desired_size = conf['AutoScalingGroups'][n]['DesiredCapacity']
			zoneidentifier = conf['AutoScalingGroups'][n]['VPCZoneIdentifier']

			#'for' loop to initialize list of load balancer names
			load_balancer_names = []
			for i in range(len(conf['AutoScalingGroups'][n]['LoadBalancerNames'])):
				load_balancer_names.append(conf['AutoScalingGroups'][n]['LoadBalancerNames'][i])
			#'for' loop to initialize list of termination policies
			#termination_policies = []
			#for i in range(len(conf['AutoScalingGroups'][n]['TerminationPolicies'])):
			#	termination_policies.append(conf['AutoScalingGroups'][n]['TerminationPolicies'][i])
		
		except KeyError, e: # If variable missed from conf file
			print "Please check your 'environment.json' config file."
			print "ASG: %s" % asg_names[n]
			print "The problem: %s." % e
			sys.exit(1)


		print "Creating Auto Scaling Group: %s" %  asg_names[n]
		print asg_names[n], launch_conf_name, min_size, max_size, desired_size, load_balancer_names

		client_asg.create_auto_scaling_group(
		AutoScalingGroupName=asg_names[n],
		LaunchConfigurationName=launch_conf_name,
		MinSize=min_size,
		MaxSize=max_size,
		DesiredCapacity=desired_size,
		VPCZoneIdentifier=zoneidentifier,
		LoadBalancerNames=load_balancer_names
		)


def create_elb(elb_names):
			
	#Creating Load Balancers
	for n in range(len(elb_names)):

		subnets = conf['LoadBalancer'][n]['Subnets']
		print subnets

		print "Creating Load Balancer: %s" %  elb_names[n]

		# 'for' loop to initialize list of protocols/ports for ELB and Instances attached
		for i in range(len(conf['LoadBalancer'][n]['Listeners'])):
			listener_elb_protocol = conf['LoadBalancer'][n]['Listeners'][i]["Protocol"]
			listener_elb_port = conf['LoadBalancer'][n]['Listeners'][i]["LoadBalancerPort"]
			listener_instance_protocol = conf['LoadBalancer'][n]['Listeners'][i]["InstanceProtocol"]
			listener_instance_port = conf['LoadBalancer'][n]['Listeners'][i]["InstancePort"]			

			if i == 0:
				client_elb.create_load_balancer(
				LoadBalancerName=elb_names[n],
				Listeners=[
					{
					'Protocol': listener_elb_protocol,
					'LoadBalancerPort': listener_elb_port,
					'InstanceProtocol': listener_instance_protocol,
					'InstancePort': listener_instance_port
					}
					],
				Subnets = subnets)

			elif i > 0:
				client.create_load_balancer_listeners(
					LoadBalancerName=elb_names[n],
					Listeners=[
						{
						'Protocol': listener_elb_protocol,
						'LoadBalancerPort': listener_elb_port,
						'InstanceProtocol': listener_instance_protocol,
						'InstancePort': listener_instance_port
						}
						],
						)

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


def remove_elb(elb_names):
	
	#Removing ELBs
	for elb_name in elb_names:
		print "Removing Load Balancer: %s" % elb_name
		client_elb.delete_load_balancer(LoadBalancerName=elb_name)


#=========Tidy_up_configuration=================================================
def config_changes():
	pass

#=========Main==================================================================

#stop_asg(['BE_asg-001','FE_asg-001'])
#start_asg(['BE_asg-001','FE_asg-001'])

#create_launch_conf(launch_conf_names)
#remove_launch_config(launch_conf_names)

#create_elb(elb_names)
#remove_elb(elb_names)

#create_asg(asg_names)
#remove_asg()


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
	create_elb(elb_names)
	create_asg(asg_names)
	
elif args[1] == "remove":
	pass
