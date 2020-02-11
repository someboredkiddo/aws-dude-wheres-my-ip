import argparse

import boto3


def find_ip_in_cluster(ip):
    client = boto3.client('ecs', region_name='us-east-1')

    cluster_paginator = client.get_paginator('list_clusters')
    cluster_page_iterator = cluster_paginator.paginate()
    for cluster_page in cluster_page_iterator:
        clusters = cluster_page.get('clusterArns')

        for cluster in clusters:
            # print('Searching cluster {}'.format(cluster))
            task_arns = client.list_tasks(cluster=cluster).get('taskArns')
            if not task_arns:
                continue
            tasks = client.describe_tasks(cluster=cluster, tasks=task_arns).get('tasks')

            for task in tasks:
                attachments = task.get('attachments')
                for attachment in attachments:
                    attachment_details = attachment.get('details')
                    for detail in attachment_details:
                        # print(detail)
                        # name == 'privateIPv4Address'
                        if detail.get('value') == ip:
                            return cluster
    return None


def find_ip_in_ec2(ip):
    client = boto3.client('ec2', region_name='us-east-1')
    response = client.describe_instances(
            Filters=[
        {
                'Name': 'network-interface.addresses.private-ip-address',
                'Values': [
                    ip,
                ]
        },
    ])

    reservations = response.get('Reservations')

    if len(reservations) == 0:
        return None

    ec2_instance = reservations.pop().get('Instances').pop()
    instance_id = ec2_instance.get('InstanceId')

    tags = ec2_instance.get('Tags')
    instance_name = None
    for tag in tags:
        if tag['Key'] == 'Name':
            instance_name = tag['Value']

    return (instance_id, instance_name)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    args = parser.parse_args()
    print('Looking for Cluster with IP {}'.format(args.ip))
    cluster = find_ip_in_cluster(args.ip)
    if cluster:
        print('Found IP in task on cluster: {}'.format(cluster))
        exit(0)
    print('IP not found in any ECS cluster\n')

    print('Looking for ec2 instance with IP {}'.format(args.ip))
    ec2_instance = find_ip_in_ec2(args.ip)
    if ec2_instance:
        print('Found IP on ec2 instance: {} {}'.format(ec2_instance[0], ec2_instance[1]))
        exit(0)
    print('IP not found in any ec2 instance')
    exit(1)
