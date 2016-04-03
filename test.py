'''## Test Python Script

import boto3

client = boto3.client('autoscaling')
asg_describe = client.describe_auto_scaling_groups(AutoScalingGroupNames=['BE_asg-002'])

current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']

#asg_instances_ids = asg_describe['AutoScalingGroups'][0]['Instances'][0:1]['InstanceId']

print current_max_size,current_min_size,current_desired_size

if current_max_size > 0 and current_desired_size > 0:
        print "Seems like instances in ASG: already stopped"
        #sys.exit(1)

#client.update_auto_scaling_group(AutoScalingGroupName='BE_asg-002',MinSize=0,MaxSize=2,DesiredCapacity=2)

#print asg_instances_ids
'''
#============================================== TEST functions ===============================================

import boto3

def stop_asg(asg_names):
	
	#usage: stop_asg(['BE_asg-002'])
    
    # for loop to stop each ASG
	for asg_name in asg_names:
	    
	    #Needed info from config file
	    #ASG_NAME_FROM_CONF = []

		client = boto3.client('autoscaling')
		asg_describe = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
		current_min_size = asg_describe['AutoScalingGroups'][0]['MinSize']
		current_max_size = asg_describe['AutoScalingGroups'][0]['MaxSize']
		current_desired_size = asg_describe['AutoScalingGroups'][0]['DesiredCapacity']

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

stop_asg(['FE_asg-002','BE_asg-002'])
