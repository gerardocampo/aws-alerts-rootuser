# aws-alerts-rootuser

### Purpose:
🛑 It is advised not to use the AWS Root account[^1], except for tasks that require it.[^2]
👮  Now with this, you can get **email alerts** *whenever the AWS Root account is used*.


## **IMPORTANT BEFORE YOU USE THIS**:  ⚠️
  
  ### FIRST: 
1. **Zip** up Python file __*RootActivityLambda.py*__, and **upload** ⤴️ the **zip** file to S3.
  - *Command in macOS:*  
  ```
  zip -r -X RootActivityLambda.zip RootActivityLambda.py
  ```
  - Upload this __*RootActivityLambda.zip*__ file to your S3 bucket 🪣 in this AWS account. 
  
  
  ### THEN: 
2. **Specify 👀 where the S3 bucketname and path of the zip** file is, in the CF template.
  - In the CFN file __*RootActivity.yaml*__, find the `AWS::Lambda::Function` function, and update the values for `S3Bucket` 🪣 and `S3Key` 🗝️.
    - NOTE: 
      - `S3Bucket` 🪣 is the name of the S3 bucket you uploaded the file to. 
      - `S3Key` 🗝️ is the path and filename. 
    - _So for example_... if the path of where you uploaded to is `S3:\\lmbda-functions\CF\RootActivityLambda.zip`, 
      - _then_ `S3Bucket: lmbda-functions` 
      - **_and,_** `S3Key: CF/RootActivityLambda.zip`
  
  ### LASTLY: 
3. Enter the **email address**(es) to receive the notifications. 
  - In the file *RootActivity.yaml*, find the `EmailSubscription` (or `AWS::SNS::Subscription`) section(s), 
    - _as needed_, **uncomment** #️⃣👀 and add additional SNS 📨 subscriptions, 
    - and check/update the value of the `Endpoint:` key.  
    - **SAVE IT.** 🏦


## Now, you're READY TO DEPLOY: 🦾🤓
  if you're using AWS CLI and invoking CF, 
  you'll need the `CAPABILITY_IAM` & `CAPABILITY_NAMED_IAM` capabilities: ✔️

```
aws cloudformation create-stack --stack-name AWSRootUserAlerts \
  --template-body file://RootActivity.yaml \
  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"
```
  
## For Troubleshooting  🛠️ 🧐

- *If need be*, enable debugging: go to Lambda --> Functions --> `NameOfCFStack`Function, and uncomment #️⃣ out the `logger.debug` lines in the Python script.
- **But definitely go to** CloudWatch --> Log groups --> /aws/lambda/`NameOfCFStack`.

## Information & References 📖
This CloudFormation template will use a .Zip file archive in an S3 bucket, which has a Python Lambda function[^3], 
and will provision the following resources:
  
- CF Stack
- EventBridge Rule
- SNS Topic + Subscription(s)
- Lambda Function & Application
- IAM Role + In-line Policy (for Lambda Function)
  
  
The CFN template & Lambda package is based on:
- https://aws.amazon.com/premiumsupport/knowledge-center/root-user-account-eventbridge-rule/
- https://aws.amazon.com/blogs/mt/monitor-and-notify-on-aws-account-root-user-activity/
  
  

------------------------------------------------------------

"Prevention is ideal. But Detection is an absolute must."

"The eyes of the Lord are in every place, 
  Keeping watch on the evil and the good."
  ~ Proverbs 15:3



[^1]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html
[^2]: https://docs.aws.amazon.com/general/latest/gr/root-vs-iam.html#aws_tasks-that-require-root
[^3]: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
