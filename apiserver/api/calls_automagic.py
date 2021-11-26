import yaml
from pprint import pprint
from oim_logging import get_oim_logger


def validateYML(body):
    log = get_oim_logger()
    log.debug(f'Initial type of body is {type(body)}')
    try:
        parsed_yaml = yaml.load(body)
        pprint(parsed_yaml)
    except BaseException:
        return 'Bad yaml syntax', 400

    if not parsed_yaml.get('apiVersion', None):
        return 'Missing apiVersion', 422
    if not parsed_yaml.get('kind', None):
        return 'Missing kind', 422
    return 'Validation OK', 200
