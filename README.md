# aws-dude-wheres-my-ip

this script search both ecs and ec2 clusters for an IP

```
python ./find_aws_ip.py 10.1.2.3

Looking for Cluster with IP 10.1.2.3
IP not found in any ECS cluster

Looking for ec2 instance with IP 10.1.2.3
Found IP on ec2 instance: i-abcdefghic dev-instance-name
```
