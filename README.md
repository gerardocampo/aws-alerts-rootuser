# aws-alerts-rootuser

Purpose:
It is advised not to use the AWS Root account, except for tasks that require it.[^1]

With this, email alerts will be sent whenever the AWS Root account is used.

This CloudFormation template will use a .Zip file archive in an S3 bucket, which has a Python Lambda function[^2], 
and will create the following resources:
- CF Stack
- EventBridge Rule
- SNS Topic & Subscription(s)
- Lambda Function & Application
- IAM Role & In-line Policy (for Lambda Function)

The CFN template is based on:
- https://aws.amazon.com/premiumsupport/knowledge-center/root-user-account-eventbridge-rule/
And the Lambda Python package is based on:
- https://aws.amazon.com/blogs/mt/monitor-and-notify-on-aws-account-root-user-activity/

_BEFORE YOU USE THIS_:  

In the `RootActivity.yaml` file, update the `EmailSubscription` section(s), particularly the `Endpoint:` value(s).

When invoking CF via CLI, you'll need the "CAPABILITY_IAM" & "CAPABILITY_NAMED_IAM" capabilities:

`aws cloudformation create-stack --stack-name AWSRootUserAlerts --template-body file://RootActivity.yaml --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"`


[^1]: - https://docs.aws.amazon.com/general/latest/gr/root-vs-iam.html#aws_tasks-that-require-root
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html

[^2]: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
