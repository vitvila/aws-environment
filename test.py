'''## Test Python Script

import boto3
import time

client = boto3.client('autoscaling')
client_ec2 = boto3.client('ec2')


asg_describe = client.describe_auto_scaling_groups(AutoScalingGroupNames=['BE_asg-002'])

current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']
instances = []
inst_statuses = []


#for n in range(len(asg_describe['AutoScalingGroups'][0]['Instances'])):
#	instances.append(asg_describe['AutoScalingGroups'][0]['Instances'][n]['InstanceId'])

#response = client_ec2.describe_instance_status(InstanceIds=instances)
for n in range(len(asg_describe['AutoScalingGroups'][0]['Instances'])):
	instances.append(asg_describe['AutoScalingGroups'][0]['Instances'][n]['InstanceId'])
	#inst_statuses.append(response['InstanceStatuses'][n]['InstanceState']['Name'])

print instances

#print client_ec2.describe_instances(InstanceIds=['i-e261e168'])['Reservations'][0]['Instances'][0]['State']['Name']

for instance in instances:
	inst_statuse = 'running'
	while inst_statuse == 'running':
		inst_statuse = client_ec2.describe_instances(InstanceIds=[instance])['Reservations'][0]['Instances'][0]['State']['Name']
		print "Instance_id: %s is still running" % instance
		time.sleep( 3 )

	print inst_statuse
	 
	
print current_max_size,current_min_size,current_desired_size
'''
#============================================== TEST functions ===============================================

import boto3
import time

def stop_asg(asg_names):
	
	#usage: stop_asg(['BE_asg-002'])
    
    # for loop to stop each ASG
	for asg_name in asg_names:
	    
	    #Needed info from config file
	    #ASG_NAME_FROM_CONF = []

		client = boto3.client('autoscaling')
		client_ec2 = boto3.client('ec2')
		asg_describe = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
		current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
		current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
		current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']
		#Creating list of instance ids for runnig servers in asg
		instances = []
		for n in range(len(asg_describe['AutoScalingGroups'][0]['Instances'])):
			instances.append(asg_describe['AutoScalingGroups'][0]['Instances'][n]['InstanceId'])

		print "Stopping ASG: %s" % asg_name

		#Checking if instances already stopped
		if current_max_size == 0 and current_desired_size == 0:
			print "Seems like instances in ASG: %s already stopped" % asg_name
			continue

		client.update_auto_scaling_group(
		AutoScalingGroupName=asg_name,
		MinSize=0,
		MaxSize=0,
		DesiredCapacity=0)

		#Checking whether instances changed state to != 'running'
		for instance in instances:
			inst_statuse = 'running'
			while inst_statuse == 'running':
				inst_statuse = client_ec2.describe_instances(InstanceIds=[instance])['Reservations'][0]['Instances'][0]['State']['Name']
				print "Instance_id: %s is still running. Waiting for it to be stopped." % instance
				time.sleep( 30 )

		print "Environment successfully stopped."

stop_asg(['BE_asg-002'])