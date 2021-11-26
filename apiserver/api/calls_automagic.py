import yaml
from pprint import pprint


def validateYML(body):
    try:
        parsed_yaml = yaml.safe_load(body)
    except BaseException:
        return 400, 'Bad yaml syntax'

    if not parsed_yaml.get('apiVersion', None):
        return 422, 'Missing apiVersion'
    if not parsed_yaml.get('kind', None):
        return 422, 'Missing kind'
    return 200, 'Validation OK'
