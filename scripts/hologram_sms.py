# hologram_sms.py - Hologram Python SDK command line interface (CLI) for sending SMS
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
#
# LICENSE: Distributed under the terms of the MIT License

import argparse
import sys
import hjson

sys.path.append(".")
sys.path.append("..")

import Hologram
from Hologram.HologramCloud import HologramCloud

script_description = '''
This hologram_send program sends a message (string) to the cloud
'''

def parseArguments():

    parser = argparse.ArgumentParser(description = script_description)

    parser.add_argument("message", nargs = '?',
                        help = 'SMS payload that will be sent to the destination number')

    parser.add_argument('--cloud_id', nargs = '?',
                        help = 'Hologram cloud ID (4 characters long)')

    parser.add_argument('--cloud_key', nargs = '?',
                        help = 'Hologram cloud Key (4 characters long)')

    parser.add_argument('--destination', nargs = '?',
                        help = 'The destination number in which the SMS will be sent')

    parser.add_argument('-f', '--file', nargs = '?',
                        help = 'Configuration (HJSON) file that stores the required credentials to send SMS')

    return parser.parse_args()

def main():

    args = parseArguments()

    if args.file:
        data = None
        with open(args.file) as credentials_file:
            data = hjson.load(credentials_file)

        if not args.cloud_id:
            args.cloud_id = data['cloud_id']

        if not args.cloud_key:
            args.cloud_key = data['cloud_key']

    if not args.message:
        raise Exception('A SMS message body must be provided')
    elif not args.destination:
        raise Exception('A destination number must be provided in order to send SMS to it')

    credentials = {'cloud_id': args.cloud_id, 'cloud_key': args.cloud_key}

    hologram = HologramCloud(credentials)
    recv = hologram.sendSMS(args.destination, args.message) # Send SMS to destination number
    print 'DATA RECEIVED: ' + str(recv)

if __name__ == "__main__": main()
