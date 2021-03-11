# oim_loggin.py
# will initialize the oim_loggin
import logging
import logging.config
# import os


def get_oim_logger():
    return logging.getLogger('oim_logger')


def init_logging(config: dict):
    # need validate check for the logging.conf
    if config.get('LOGGING_CONFIGFILE') is None:
        raise ValueError("No [logging.conf] is given by env...")
    logger_config_file = config.get("LOGGING_CONFIGFILE")

    if config.get('LOGGING_LOGFILE') is None:
        root_logger = logging.getLogger()
        root_logger.info('No [LOGGING_LOGFILE] is given by env, using [error.log] as default')

    logger_log_file = config.get("LOGGING_LOGFILE", 'error.log')

    logger_mailhost = config.get("LOGGING_MAILHOST")

    logging.config.fileConfig(logger_config_file,
                              defaults={'logfilename': logger_log_file,
                                        'mailhost': logger_mailhost,
                                        'toaddrs': 'foo@foo.ch'})
    running_logger = get_oim_logger()

    if config.get('DEBUG') == 'True':
        # set DEBUG als level on all oim_logger LOGGING
        running_logger.info('Found config DEBUG=True -> set log level DEBUG')
        running_logger.setLevel('DEBUG')
    else:
        running_logger.info('Found config DEBUG=False -> set log level INFO')
        running_logger.setLevel('INFO')


def get_oim_logger_name() -> str:
    return('oim_logger')
