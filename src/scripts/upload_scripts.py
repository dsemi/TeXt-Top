#!/usr/bin/python2

import boto, glob, os
amazon_access_key = 'AKIAIUW65R6HVR3RNJFQ'
amazon_secret_key = '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'

current_dir = os.path.dirname(__file__)
if current_dir:
    os.chdir(current_dir)

s3 = boto.connect_s3(amazon_access_key, amazon_secret_key)

bucket = s3.get_bucket('text-top')

keys = bucket.get_all_keys(prefix='windows/')
bucket.delete_keys(keys)

keys = bucket.get_all_keys(prefix='linux/')
bucket.delete_keys(keys)

for i in glob.glob('windows/*'):
    k = bucket.new_key(i)
    k.set_contents_from_filename(i)

for i in glob.glob('linux/*'):
    k = bucket.new_key(i)
    k.set_contents_from_filename(i)
