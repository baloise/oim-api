# oim_loggin.py
# will initialize the oim_loggin
import logging
import logging.config
import os


def init_logging(config=os.environ):  # TODO: Rework this function. A lot of testing code leftover
    if config.get('DEBUG', False):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

    logging.debug("Exists:", "config" in globals())

    if config.get('LOGGING_CONFIGFILE') is not None:
        logging.debug("The [{}] is present.\n".format("LOGGING_CONFIGFILE"))
    else:
        logging.debug("The [{}] does not exist in the dictionary.".format("LOGGING_CONFIGFILE"))
    logger_config_file = config.get("LOGGING_CONFIGFILE")
    logging.debug('LOGGING_CONFIGFILE:{}'.format(logger_config_file))
    logger_log_file = config.get("LOGGING_LOGFILE")
    logging.debug('LOGGING_LOGFILE:{}'.format(logger_log_file))
    logger_mailhost = config.get("LOGGING_MAILHOST")
    logging.debug('LOGGING_MAILHOST:{}'.format(logger_mailhost))
    logging.config.fileConfig(logger_config_file,
                              defaults={'logfilename': logger_log_file,
                                        'mailhost': logger_mailhost,
                                        'toaddrs': 'foo@foo.ch'})
