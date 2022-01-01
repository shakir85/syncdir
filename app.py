#!/bin/python3
from core import syncdir
from argparse import ArgumentParser


if __name__ == '__main__':

    parser = ArgumentParser(prog='PROG',
                            description='''Versatile script to sync, copy, and compress files.
                            sync is implemented via rsync with preserving files permissions. 
                            You need to create a log directory in /var/log/syncdir 
                            and you need to give the executing user permissions to write to this directory.''')
    parser.add_argument('-d', '--dest', required=True, help='Absolute path to backup directory - no trailing forward-slash')
    parser.add_argument('-s', '--src', required=True, help='Absolute path to source directory - no trailing forward-slash')
    parser.add_argument('-c', '--compress', required=False, help='To compress backup directory. If you intended to run'
                                                           'the script as a scheduled task (i.e. cron), '
                                                           'then this option will force rsync to '
                                                           'always perform files sync across all the files'
                                                           'rather than synchronizing the deltas only.')
    parser.add_argument('-n', '--job-name', required=True,
                        help="Sync job name. It's required not for functional reasons, just for logging purposes..")
    parser.add_argument('--dry-run', required=False, help='Dry run sync task')
    args = parser.parse_args()

    """---- Execution Block ----"""
    if args.dry_run:
        syncdir.backup(destination=args.dest, source=args.src, job_name=args.job_name, dry_run=args.dry_run)
    else:
        syncdir.backup(destination=args.dest, source=args.src, job_name=args.job_name)

    # # Arbitrary sleep to ensure backup & compress execution don't overlap
    # time.sleep(8)
    # if args.compress:
    #     core.compress()
