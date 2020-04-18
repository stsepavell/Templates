import logging
from .module1 import module1_main



##########  Module Properties  ####################

logger = logging.getLogger(__name__)



##########  Functions  ############################

def run(main_config):
    logger.info("this is app main")
    module1_main.module1_func()



##########  Main  #################################

if __name__ == "__main__":
    raise Exception('This module is not intended to run as __main__')
