# aws-alerts-rootuser

Purpose:
It is advised not to use the AWS Root account[^1], except for tasks that require it.[^2]

With this, email alerts will be sent whenever the AWS Root account is used.

This CloudFormation template will use a .Zip file archive in an S3 bucket, which has a Python Lambda function[^3], 
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


**IMPORTANT BEFORE YOU USE THIS**:  

In the `RootActivity.yaml` file, update the `EmailSubscription` section(s), particularly the `Endpoint:` value(s).


## When you're ready to deploy
  if you're using AWS CLI and invoking CF, 
  you'll need the `CAPABILITY_IAM` & `CAPABILITY_NAMED_IAM` capabilities:

```
aws cloudformation create-stack --stack-name AWSRootUserAlerts \
  --template-body file://RootActivity.yaml \
  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"
```

------------------------------------------------------------

"Prevention is ideal. But Detection is an absolute must."

>"The eyes of the Lord are in every place, 
>Keeping watch on the evil and the good."
> - Proverbs 15:3



[^1]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html
[^2]: https://docs.aws.amazon.com/general/latest/gr/root-vs-iam.html#aws_tasks-that-require-root
[^3]: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
