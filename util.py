#!/usr/bin/env python2

import time
import boto3

region = 'ap-southeast-2'
ec2_client = boto3.client('ec2', region_name=region)
ec2_resource = boto3.resource('ec2', region_name=region)

class Util():
  def status(self, instance):
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    return a['Reservations'][0]['Instances'][0]['State']['Name']

  def stop(self, instance):
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    id = a['Reservations'][0]['Instances'][0]['InstanceId']
    print('Instance stopping')
    ec2_resource.Instance(id).stop()
    while self.status(instance) != 'stopped':
      # Wait untill the instance is running
      time.sleep(1)
    print('Instance stopped.')

  def start(self, instance):
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    id = a['Reservations'][0]['Instances'][0]['InstanceId']
    print('Instance starting')
    ec2_resource.Instance(id).start()
    while self.status(instance) != 'running':
      # Wait untill the instance is running
      time.sleep(1)
    print('Instance started.')

  def reboot(self, instance):
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    id = a['Reservations'][0]['Instances'][0]['InstanceId']
    ec2_resource.Instance(id).reboot()

  def get_size(self, instance):
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    return a['Reservations'][0]['Instances'][0]['InstanceType']

  def get_size(self, instance):
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    return a['Reservations'][0]['Instances'][0]['InstanceType']

  def change_size(self, instance, size):
    valid_sizes = ['t2.xlarge',
                   't2.small',
                   't2.micro',
                   't2.medium',
                   't2.large',
                   't2.2xlarge',
                   'r4.xlarge',
                   'r3.xlarge',
                   'r3.large',
                   'm5.xlarge',
                   'm4.xlarge',
                   'm4.large',
                   'm4.4xlarge',
                   'm4.2xlarge',
                   'm3.xlarge',
                   'm3.medium',
                   'm3.large',
                   'c4.xlarge',
                   'c4.8xlarge',
                   'c4.2xlarge',]
    a = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance, ]},],)
    id = a['Reservations'][0]['Instances'][0]['InstanceId']

    if size in valid_sizes:
      if size == self.get_size(instance):
        return True
      else:
        print('Current size: %s\nNew size: %s' % (self.get_size(instance), size))
        if self.status(instance) != 'stopped':
          self.stop(instance)
        ec2_client.modify_instance_attribute(InstanceId=id, InstanceType={'Value': size },)
        print('Resizing...')
        while self.get_size(instance) != size:
          print('Current size: %s\nNew size: %s' % (self.get_size(instance), size))
          time.sleep(1)
      self.start(instance)
    else:
      print('Invalid size. Valid sizes are %s.' % (valid_sizes))
      return False
