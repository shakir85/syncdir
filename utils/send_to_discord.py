import datetime
import logging
from http.client import HTTPException
from discord import Webhook, RequestsWebhookAdapter, Embed, NotFound, Forbidden
"""
colors:
    teal -> 0x1abc9c
    green -> 0x2ecc71
    red -> 0xe74c3c
"""

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename="/var/log/syncdir/syncdir.log", filemode="a")


def success_job(webhook_url, job_name):
    now = datetime.datetime.now()
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
    embed = Embed(timestamp=now.now(), tilte="rsync backup", description="[OK] complete", color=0x2ecc71)
    try:
        msg = webhook.send(embed=embed, content=f"Files have been backed up successfully for job {job_name}")
        logging.info("Success message was sent to Discord channel")
        return msg
    except HTTPException as h:
        logging.error(f"Sending message to discord failed\n{h}")
    except NotFound as nf:
        logging.error(f"The entered webhook was not found\n{nf}")
    except Forbidden as fb:
        logging.error(f"The authorization token for the webhook is incorrect\n{fb}")


def failed_job(webhook_url, job_name):
    now = datetime.datetime.now()
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
    embed = Embed(timestamp=now.now(), tilte="rsync backup", description="[Alert] failed", color=0xe74c3c)
    try:
        msg = webhook.send(embed=embed, content=f"Rsync backup failed for job {job_name}")
        logging.info("Success message was sent to Discord channel")
        return msg
    except HTTPException as h:
        logging.error(f"Sending message to discord failed\n{h}")
    except NotFound as nf:
        logging.error(f"The entered webhook was not found\n{nf}")
    except Forbidden as fb:
        logging.error(f"The authorization token for the webhook is incorrect\n{fb}")



