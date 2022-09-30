#####################################################################################################
#
# ABOUT
#
#  This Lambda function sends an SNS notification to a given AWS SNS topic
#	when an event in CloudTrail by the AWS Root user is detected.  It based on:
#  	https://aws.amazon.com/blogs/mt/monitor-and-notify-on-aws-account-root-user-activity/
#
#  And relies on a CloudFormation template, based on:
#	https://aws.amazon.com/premiumsupport/knowledge-center/root-user-account-eventbridge-rule/
#
#   Together, the CF template & the Lambda function/application will provision the following resources:
#		* CF Stack
#		* EventBridge Rule
#		* SNS Topic & Subscriptions
#		* Lambda Function & Application
#		* IAM Role & In-line Policy (for Lambda Function)
#
####################################################################################################
#
# VERSION HISTORY
#    Original authored by Sudhanshu Malhotra, AWS.
#    1.0, 18-Sept-2022, Gerard Ocampo
#	 1.1  29-Sept-2022, Gerard Ocampo - updated email body.
#
####################################################################################################

import json
import boto3
import logging
import os
import botocore.session
from botocore.exceptions import ClientError
session = botocore.session.get_session()

logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)

def lambda_handler(event, context):
	eventname = event['detail']['eventName']
	snsARN = os.environ['SNSARN']          #Getting the SNS Topic ARN passed in by the environment variables.
	user = event['detail']['userIdentity']['type']
	eventsource = event['detail']['eventSource']
	eventtime = event['detail']['eventTime']
	eventid = event['detail']['eventID']
	sourceip = event['detail']['sourceIPAddress']
	useragent = event['detail']['userAgent']
	account = event['account']
	source = event['source']

	MsgJson = json.dumps(event, indent = 4)

	#Debugging logs go to CloudWatch Logs
	#logger.setLevel(logging.DEBUG)
	#logger.debug("Event is --- %s" %event)
	#logger.debug("Event Name is--- %s" %eventname)
	#logger.debug("SNSARN is-- %s" %snsARN)
	#logger.debug("User Name is -- %s" %user)

	client = boto3.client('iam')
	snsclient = boto3.client('sns')
	response = client.list_account_aliases()
	#logger.debug("List Account Alias response --- %s" %response)

	try:
		if not response['AccountAliases']:
			accntAliase = (boto3.client('sts').get_caller_identity()['Account'])
			logger.info("Account Aliase is not defined. Account ID is %s" %accntAliase)
		else:
			accntAliase = response['AccountAliases'][0]
			logger.info("Account Aliase is : %s" %accntAliase)

	except ClientError as e:
		logger.error("Client Error occured")

	MsgHuman = "Greetings Zelis Human: \n\nPlease be advised, activity has been detected for the AWS *root* user (in account alias %s, account #: %s).\n\nIt is not recommended to use the Root account, except for tasks that require it.\n\nIMPORTANT: If this activity is unexpected, please follow-up ASAP and respond accordingly.\n\nEvent Summary:\n\teventName: %s\n\tnotificationSource: %s\n\tsourceIP: %s\n\tuserAgent: %s\n\tdate/time: %s\n\tCloudTrail eventID: %s\n\nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html\nhttps://docs.aws.amazon.com/general/latest/gr/root-vs-iam.html#aws_tasks-that-require-root\n\n" % (accntAliase, account, eventname, source, sourceip, useragent, eventtime, eventid)
	BufferHumanJson = "......................................... Below is data of the event that triggered this notification. ............................................"
	Msg = MsgHuman + "\n" + BufferHumanJson + "\n\n" + MsgJson

	try:
		#Sending the notification...
		snspublish = snsclient.publish(
						TargetArn= snsARN,
						Subject=(("Root Account Activity Detected - in AWS \"%s\": %s" %(accntAliase, eventname))[:100]),
						Message=Msg
						)

	#	logger.debug("SNS publish response is-- %s" %snspublish)
	except ClientError as e:
		logger.error("An error occured: %s" %e)
