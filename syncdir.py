#!/bin/python3
import time
import logging
from argparse import ArgumentParser
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
"""
    Script to rsync everything in a directory
"""


def backup():
    try:
        # Run in a targeted user's cron
        # rsync will copy the content of "/home/$USER" but not the $USER directory itself
        rsync = f"rsync -Ccavz --delete {args.src} {args.dest}"
        process = Popen(rsync, shell=True, stdout=PIPE, stderr=STDOUT)

        with process.stdout:
            for i in iter(process.stdout.readline, b''):
                logging.info(i.decode("utf-8").strip())

    except OSError as e:
        logging.error(f"backup() - Failed to run rsync\n{e}")


def compress():
    today = datetime.today().strftime('%b-%d-%Y')
    try:
        # Compress on place
        tar_file = f"{args.dest}/{today}-backup.tar.gz"
        tar = f"tar czf {tar_file} --absolute-names {args.dest}"
        process = Popen(tar, shell=True, stdout=PIPE, stderr=STDOUT)

        with process.stdout:
            for i in iter(process.stdout.readline, b''):
                logging.info(i.decode("utf-8").strip())

    except OSError as e:
        logging.error(f"compress() - Failed to compress backup\n{e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename="/var/log/syncdir/syncdir.log", filemode="a")

    parser = ArgumentParser(prog='PROG',
                            description='''Script to backup and compress a directory using rsync.
                            Designed to run in a cron job. 
                            You need to create a log directory in /var/log/syncdir 
                            and you need to give the executing user permission to write to this directory.''')
                            
    parser.add_argument('--dest', required=True, help='Path to backup destination directory - no trailing forward-slash')
    parser.add_argument('--src', required=True, help='Path to backup source directory - no trailing forward-slash')
    parser.add_argument('--compress', required=False, help='Compress backup directory '
                                                           '(This will force rsync to always copy all the files'
                                                           'rather than copying deltas only).')

    args = parser.parse_args()

    backup()
    logging.info("Backup completed.")
    # Arbitrary sleep
    time.sleep(8)
    if args.compress:
        compress()
        logging.info("Backup compressed.")
