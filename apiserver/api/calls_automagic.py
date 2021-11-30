import yaml
import re
# from pprint import pprint
from oim_logging import get_oim_logger


def validateYML(body):
    valid_apiVersion = ['v1alpha1']
    valid_kind = ['VirtualMachine']
    valid_status = ['active', 'decommisioned', 'deleted']

    log = get_oim_logger()
    log.debug(f'Initial type of body is {type(body)}')
    try:
        parsed_yaml = yaml.load(body, Loader=yaml.SafeLoader)
        # pprint(parsed_yaml)
    except BaseException:
        return 'Bad yaml syntax', 400

    apiVersion = parsed_yaml.get('apiVersion', None)
    if not apiVersion:
        return 'Missing apiVersion', 422
    if apiVersion not in valid_apiVersion:
        return 'Unsupported apiVersion', 422

    kind = parsed_yaml.get('kind', None)
    if not kind:
        return 'Missing kind', 422
    if kind not in valid_kind:
        return 'Unsupported kind', 422

    metadata = parsed_yaml.get('metadata', None)
    if not metadata:
        return 'Missing metadata section', 422

    spec = parsed_yaml.get('spec', None)
    if not spec:
        return 'Missing spec section', 422

    status = spec.get('status', None)
    if not status:
        return 'Missing status', 422
    if status not in valid_status:
        return 'Invalid status', 422

    pattern_uuid = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$', re.IGNORECASE)
    id = spec.get('id', None)
    if not id:
        return 'Missing id', 422
    if not pattern_uuid.match(str(id)):
        return 'id does not conatain a valid UUID(v4)', 422

    return 'Validation OK', 200
