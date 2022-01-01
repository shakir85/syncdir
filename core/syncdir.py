#!/bin/python3
import os
import logging
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from utils import send_to_discord
"""
    Script to rsync everything in a directory
    DISCORD_WEBHOOK environment variable need to be exported 
    to send sync fail/success notifications to Discord.
"""

# TODO: Add 3,2,1 strategy copy & compress function
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                        filename="/var/log/syncdir/syncdir.log", filemode="a")


def copy():
    pass


def backup(destination, source, job_name, dry_run=False):
    try:
        # rsync will copy the 'content' of the directory but not the directory itself
        rsync = f"rsync -Ccavz --delete {source} {destination}"
        rsync_dry_run = f"rsync -Ccavz --dry-run -delete {source} {destination}"

        if dry_run:
            process = Popen(rsync_dry_run, shell=True, stdout=PIPE, stderr=STDOUT)
            logging.info("Running rsync in Dry-Run mode...")
        else:
            process = Popen(rsync, shell=True, stdout=PIPE, stderr=STDOUT)

        with process.stdout:
            for i in iter(process.stdout.readline, b''):
                logging.info(i.decode("utf-8").strip())

        # Logging & Notification
        logging.info(f"{job_name}, Backup completed")

        if DISCORD_WEBHOOK:
            send_to_discord.success_job(webhook_url=DISCORD_WEBHOOK, job_name=job_name)

    except OSError as e:
        logging.error(f"backup() - Failed to run rsync\n{e}")
        if DISCORD_WEBHOOK:
            send_to_discord.failed_job(webhook_url=DISCORD_WEBHOOK, job_name=job_name)


def compress(destination, job_name, dry_run=False):
    today = datetime.today().strftime('%b-%d-%Y')
    try:
        # Compress on place
        tar_file = f"{destination}/{today}-backup.tar.gz"
        tar = f"tar czf {tar_file} --absolute-names {destination}"
        process = Popen(tar, shell=True, stdout=PIPE, stderr=STDOUT)

        with process.stdout:
            for i in iter(process.stdout.readline, b''):
                logging.info(i.decode("utf-8").strip())

        # Logging & Notification
            logging.info(f"{job_name}, compress completed.")

        if DISCORD_WEBHOOK:
            send_to_discord.success_job(webhook_url=DISCORD_WEBHOOK, job_name=job_name)

    except OSError as e:
        logging.error(f"compress() - Failed to compress backup\n{e}")
        if DISCORD_WEBHOOK:
            send_to_discord.failed_job(webhook_url=DISCORD_WEBHOOK, job_name=job_name)