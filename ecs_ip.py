import argparse

import boto3

def find_ip_in_cluster(ip):
    client = boto3.client('ecs', region_name='us-east-1')

    cluster_paginator = client.get_paginator('list_clusters')
    cluster_page_iterator = cluster_paginator.paginate()
    for cluster_page in cluster_page_iterator:
        clusters = cluster_page.get('clusterArns')

        for cluster in clusters:
            print('Searching cluster {}'.format(cluster))
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    args = parser.parse_args()
    print('Looking for Cluster with IP {}'.format(args.ip))
    cluster = find_ip_in_cluster(args.ip)
    if cluster:
        print('Found IP in task on cluster: {}'.format(cluster))
    else:
        print('IP not found')
