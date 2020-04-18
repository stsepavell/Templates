# import argparse
import app.main
import json
import logging
import logging.config


from datetime import datetime
from os import path, makedirs
from ruamel.yaml import YAML



##########  Global Properties  ####################

start_time = datetime.now()
logger = None
# cmd_parser = argparse.ArgumentParser()
# cmd_parser.add_argument("--debug", "-d", help="log level: DEBUG (default is INFO)",)
# cmd_args = vars(cmd_parser.parse_args())



##########  Logger  ###############################

def setup_logger(logger_config_path='logger.json', default_level=logging.INFO, timestamp='%H-%M-%S'):

    timestamp = start_time.strftime(timestamp)

    # load logger config
    logger_config_path = path.abspath(logger_config_path)
    if path.exists(logger_config_path):
        with open(logger_config_path, 'rt') as file:
            logger_config = json.load(file)
        
        # add resolve logfiles paths
        for handler in logger_config['handlers']:
            try:
                logger_config['handlers'][handler]['filename'] = logger_config['handlers'][handler]['filename'].replace(
                    '@timestamp@',timestamp)
                logsdir = path.split(path.abspath(
                    logger_config['handlers'][handler]['filename']))[0]
            except:
                pass

        # create logs directory
        if not path.exists(logsdir):
            makedirs(logsdir, exist_ok=True)

        # apply logger config
        logging.config.dictConfig(logger_config)

    else:
        logging.basicConfig(level=default_level)



##########  Main  #################################

def main():

    # load main config
    yaml = YAML(typ='safe')
    with open(path.abspath('config/main.yml'), 'r') as file:
        main_config = yaml.load(file)    

    # setup logger
    setup_logger(
        logger_config_path=main_config['layout']['logger_config'], timestamp=main_config['format']['timestamp'])
    global logger
    logger = logging.getLogger(path.basename(__file__))
    logger.info('Starting application')

    # invoke main program
    try:
        app.main.run(main_config)

    except Exception as e:
        logger.exception(e)
 
if __name__ == "__main__":
    main() 
