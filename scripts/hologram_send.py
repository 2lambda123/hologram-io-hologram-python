# hologram_send.py - Hologram Python SDK command line interface (CLI) for sending messages to the cloud
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
#
# LICENSE: Distributed under the terms of the MIT License
#
import argparse
import sys
import hjson

sys.path.append(".")
sys.path.append("..")

import Hologram
from Hologram.CustomCloud import CustomCloud
from Hologram.HologramCloud import HologramCloud

script_description = '''
This hologram_send program sends a message (string) to a given host and port.
'''

def parseArguments():

    parser = argparse.ArgumentParser(description=script_description)

    parser.add_argument("message", nargs = '?',
                        help = 'message that will be sent to the cloud')

    parser.add_argument('--cloud_id', nargs = '?',
                        help = 'Hologram cloud ID (4 characters long)')

    parser.add_argument('--cloud_key', nargs = '?',
                        help = 'Hologram cloud Key (4 characters long)')

    parser.add_argument('--timeout', type = int, default = 5, nargs = '?',
                        help = 'The period in seconds before the socket closes if it doesn\'t receive a response')

    parser.add_argument('--host', default = 'cloudsocket.hologram.io', nargs = '?',
                        help = argparse.SUPPRESS)

    parser.add_argument('-p', '--port', type = int, nargs = '?',
                        default = 9999,
                        help = argparse.SUPPRESS)

    parser.add_argument('-t', '--topic', nargs = '*',
                        help = 'Topics for the message (optional)')

    parser.add_argument('-f', '--file', nargs = '?',
                        help = 'Configuration (HJSON) file that stores the required credentials to send the message to the cloud')

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

    credentials = {'cloud_id': args.cloud_id, 'cloud_key': args.cloud_key}

    # Determine which cloud type to use based on the host and port (if they are manually overriden
    recv = ''
    if args.host == 'cloudsocket.hologram.io' and args.port == 9999:
        hologram = HologramCloud(credentials)
        recv = hologram.sendMessage(args.message, topics = args.topic, timeout = args.timeout)
    else:
        customCloud = CustomCloud(credentials,
                                  send_host = args.host,
                                  send_port = args.port)
        recv = customCloud.sendMessage(args.message, timeout = args.timeout)

    print "DATA RECEIVED: " + str(recv)

if __name__ == "__main__": main()
