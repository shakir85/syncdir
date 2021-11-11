import subprocess
import logging
"""
    Script to rsync everything in a directory
"""


def backup():
    try:
        # Run in a targeted user's cron
        # rsync will copy the content of "/home/$USER" but not the $USER directory itself
        subprocess.call(["rsync", "-Ccavz", "--delete", "/home/$USER/", "/path/dest"])
    except OSError as e:
        logging.error(f"<backup> - Failed to execute \n {e}")


def compress():
    pass


def ship():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename="/var/log/dirsync.log", filemode="a")

