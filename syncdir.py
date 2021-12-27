#!/bin/python3
import time
import os
import logging
from argparse import ArgumentParser
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from toolbox import send_to_discord
"""
    Script to rsync everything in a directory
"""

# TODO: Add 3,2,1 strategy copy & compress function

def backup():
    try:
        # Run in user's cron
        # rsync will copy the 'content' of the directory but not the directory itself
        rsync = f"rsync -Ccavz --delete {args.src} {args.dest}"
        process = Popen(rsync, shell=True, stdout=PIPE, stderr=STDOUT)

        with process.stdout:
            for i in iter(process.stdout.readline, b''):
                logging.info(i.decode("utf-8").strip())

        # Logging & Notification
        if args.job_name:
            logging.info(f"{args.job_name}, Backup completed")
        else:
            logging.info("Backup completed.")

        if args.url and args.job_name:
            send_to_discord.success_job(webhook_url=os.getenv("DISCORD_WEBHOOK"), job_name=args.job_name)

    except OSError as e:
        logging.error(f"backup() - Failed to run rsync\n{e}")
        if args.url and args.job_name:
            send_to_discord.failed_job(webhook_url=os.getenv("DISCORD_WEBHOOK"), job_name=args.job_name)


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

        # Logging & Notification
        if args.job_name:
            logging.info(f"{args.job_name}, compress completed.")
        else:
            logging.info("Compress task completed.")

        if args.url and args.job_name:
            send_to_discord.success_job(webhook_url=os.getenv("DISCORD_WEBHOOK"), job_name=args.job_name)

    except OSError as e:
        logging.error(f"compress() - Failed to compress backup\n{e}")
        if args.url and args.job_name:
            send_to_discord.failed_job(webhook_url=os.getenv("DISCORD_WEBHOOK"), job_name=args.job_name)


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
    parser.add_argument('--job-name', required=False,
                        help="Sync job name to be printed in the log file. Good if running this script for multiple"
                             "backup tasks of various source/destination files.")
    args = parser.parse_args()

    # Execute
    backup()

    # Arbitrary sleep to ensure backup & compress execution don't overlap
    time.sleep(8)
    if args.compress:
        compress()