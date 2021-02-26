# oim_loggin.py
# will initialize the oim_loggin
import logging
import logging.config
from load_config import oim_config

def initLogging():
    print("Exists:", "oim_config" in globals())
    if oim_config.get('LOGGING_CONFIGFILE') != None:
            print("The [{}] is present.\n".format("LOGGING_CONFIGFILE")) 
    else:
            print("The [{}] does not exist in the dictionary.".format("LOGGING_CONFIGFILE")) 

    logger_config_file = oim_config.get("LOGGING_CONFIGFILE")
    logging.warning('LOGGING_CONFIGFILE:{}'.format(logger_config_file))
    logger_log_file = oim_config.get("LOGGING_LOGFILE")
    logging.warning('LOGGING_LOGFILE:{}'.format(logger_log_file))
    logger_mailhost = oim_config.get("LOGGING_MAILHOST")
    logging.warning('LOGGING_MAILHOST:{}'.format(logger_mailhost))
    logging.config.fileConfig(logger_config_file,
                              defaults={'logfilename': logger_log_file,
                                        'mailhost': logger_mailhost,
                                        'toaddrs': 'foo@foo.ch'})
    return

if __name__ == '__main__':
    initLogging()
