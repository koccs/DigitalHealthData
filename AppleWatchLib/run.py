# How to pass in argument to boolean variables via command line?
def str2bool(s):
    if s.lower() in ('true', 't', '1'):
        return True
    elif s.lower() in ('false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

import os
from plot_apple_watch_data import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-xml_file_path', action='store', dest='xml_file_path', help='local file path to iOS health data', type=str)
    parser.add_argument('-source_name', action='store', dest='source_name', help='Device name or app writing data to Health App', default='Apple Watch', type=str)
    parser.add_argument('-tag_name', action='store', dest='tag_name', help='XML object to parse from Health data file', default='Record', type=str)
    parser.add_argument('-start_date', action='store', dest='start_date', help='Start date (%Y-%m-%d) to filter health data timestamps')
    parser.add_argument('-end_date', action='store', dest='end_date', help='End date (%Y-%m-%d) to filter health data timestamps')
    parser.add_argument('-verbose', action='store_true', dest='verbose', help='Print out plotting status statements', default=False)
    parser.add_argument('-show_plots', action='store_true', dest='show_plots', help='Show plots into terminal/IDE', default=False)
    parser.add_argument('-save_directory', action='store', dest='save_directory', help='Local path to save plot to', default=None, type=str)

    # args = parser.parse_args()
    args = parser.parse_args(['-xml_file_path', '~/Work/export.xml',
                              '-start_date', '2020-02-10 00:00',
                              '-end_date', '2020-02-17 00:00',
                              '-source_name', 'Ádám’s Apple Watch',
                            #   '-start_date', '2020-02-01 00:00',
                            #   '-end_date', '2020-02-17 00:00',
                            #   '-source_name', 'Adams Apple Watch',
                              '-verbose',
                              '-save_directory', './results'])

    apple_watch = AppleWatchData(args.xml_file_path, args.source_name, args.start_date, args.end_date)

    # create directory to save plots
    if args.save_directory:
        if args.save_directory.startswith('~'):
            args.save_directory = os.path.expanduser(args.save_directory)
        if not os.path.exists(args.save_directory):
            os.makedirs(args.save_directory)
        os.chdir(args.save_directory)

    # create directory to save data and plots
    if not os.path.exists('apple_watch_data/'):
        os.makedirs('apple_watch_data')
    if not os.path.exists('apple_watch_plots/'):
        os.makedirs('apple_watch_plots')

    # control logging
    if not args.verbose:
        logger.propagate = False

    run(apple_watch, args.start_date, args.end_date, args.show_plots)