# Usage: /home/scripts/environment.py start|stop|restart|create|remove ENV_NAME

import sys
import boto.ec2
 

#Variables

# AWS Access Key ID
aws_key_id=''
# AWS Secret Key
aws_secret_key=''
# Region
aws_region=''
#script's arguments
args = sys.argv

#Check config/usage
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

def check_config():
	if os.path.isfile("environment.conf") == False:
		print "Please make sure you have a valid configuration file!"
		sys.exit(1)

#Start/Stop/Restart
def start_asg(env_name):
def stop_asg(env_name):
def restart_asg(env_name):

#Create/Remove
def create_asg(env_name):
def remove_asg(env_name):
def create_launch_conf(env_name):
def remove_launch_config(env_name):
def create_elb(env_name):
def remove_elb(env_name):
def config_changes(env_name):



# Main part

if args[1] == "start":
	# Config file for start ASG
	env_name = ENV_NAME 
	AutoScalingGroupName = []
	MinSize = 123
	MaxSize = 123
	
	start_asg("env_name")

elif args[1] == "stop":
	# Config file for stop ASG
	env_name = ENV_NAME
	AutoScalingGroupName = []
	MinSize = 0
	MaxSize = 0

	stop_asg()

elif args[1] == "restart":
	stop_asg("env_name")
	start_asg("env_name")

elif args[1] == "create":
	pass
elif args[1] == "remove":
	pass

# AWS random code. Archive
"""
conn_to_region = boto.ec2.connect_to_region("us-west-2", aws_access_key_id='<aws access key>', aws_secret_access_key='<aws secret key>')

#Stopping/Terminating
ec2.instances.filter(InstanceIds=ids).stop()
ec2.instances.filter(InstanceIds=ids).terminate()

# ASG
conn = boto.connect_autoscale()
config = LaunchConfiguration(name='foo', image_id='ami-abcd1234', key_name='foo.pem')
conn.create_launch_configuration(config)
