#!/usr/bin/env python

import boto3
import logging
import os
import sys



def configure_logging():
    logger = logging.getLogger(__name__)
    sh = logging.StreamHandler()
    fm = logging.Formatter('%(asctime)s %(funcName)s:%(lineno)s %(message)s')
    logger.setLevel(logging.INFO)
    sh.setFormatter(fm)
    logger.addHandler(sh)

def main():
    bucket_name = "craft485.feralmonkey.net"
    confirmation = False

    configure_logging()
    logger = logging.getLogger(__name__)

    key_path =  os.getcwd().split(os.sep)[-1]

    logger.debug(key_path)
    while confirmation != True:
        confirmation, bucket_name, key_path = confirm(confirmation, bucket_name, key_path)
    logger.info(f'Uploading to {bucket_name}/{key_path}')
    upload(bucket_name, key_path)


def confirm(confirmation, bucket_name, path):
    logger = logging.getLogger(__name__)
    logger.debug(f'conf {confirmation}')
    while confirmation != True:
        print(f'Uploading current directory to {bucket_name}/{path}')
        confirmation = input('Is this correct? [y/n]')
        if confirmation.strip() in ['Y', 'y']:
            confirmation = True
            logger.info('Uploading')
            return confirmation, bucket_name, path
        else:
            path = input('Enter the path to upload the file:')
            logger.info(f'Got {path}')
            return confirmation, bucket_name, path

def upload(bucket_name, path):
    logger = logging.getLogger(__name__)
    client = boto3.client('s3', region_name='us-east-1')
    logger.info(path)
    for root, dirs, files in os.walk('../'+path):
        logger.debug(f'root: {root}|dirs: {dirs}|files: {files}')
        for f in files:
            localpath = os.path.join(root, f)
            if 'venv' in localpath:
                continue
            if '.git' in localpath:
                continue
            if '.vscode' in localpath:
                continue
            logger.info(f'bucket_name: {bucket_name}') 
            key = f'{path}/{f}'
            logger.info(f'key: {key}')
            logging.getLogger('botocore').setLevel(logging.DEBUG)
            try:
                client.upload_file(f, bucket_name, key)
            except Exception as e:
                logger.error(f'Failed to upload to {bucket_name}')
                logger.error(e)
                logger.error(sys.exc_info()[2])


if __name__ == '__main__':
    main()