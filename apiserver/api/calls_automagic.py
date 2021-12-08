import yaml
# import re
import json
from jsonschema import validate, ValidationError
# from pprint import pprint
from oim_logging import get_oim_logger


def decide_validation_schema(inspection_object):
    # This is a dummy function for now while the validation is being worked on
    # Eventually it will return the necessary schema object depending on the given inspection object
    try:
        with open('schemas/yamlvalidation/am_postgres_schema.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None


def validateYML(body):
    valid_apiVersion = ['v1alpha1', 'automagic/v1']
    valid_kind = ['VirtualMachine', 'DB']
    # valid_status = ['active', 'decommisioned', 'deleted']

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

    # metadata = parsed_yaml.get('metadata', None)
    # if not metadata:
    #     return 'Missing metadata section', 422

    # spec = parsed_yaml.get('spec', None)
    # if not spec:
    #     return 'Missing spec section', 422

    # status = spec.get('status', None)
    # if not status:
    #     return 'Missing status', 422
    # if status not in valid_status:
    #     return 'Invalid status', 422

    # pattern_uuid = re.compile(
    #   r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$',
    #   re.IGNORECASE
    # )
    # id = spec.get('id', None)
    # if not id:
    #     return 'Missing id', 422
    # if not pattern_uuid.match(str(id)):
    #     return 'id does not conatain a valid UUID(v4)', 422

    validation_schema = decide_validation_schema(parsed_yaml)
    if not validation_schema:
        return 'Unable to decide on the validation schema to use', 422

    try:
        validate(instance=parsed_yaml, schema=validation_schema)
    except ValidationError as e:
        output_buffer = ''
        # for error in errors:
        #    for suberror in sorted(error.context, key=lambda e: e.schema_path):
        #        output_buffer = list(suberror.schema_path), suberror.message, sep=", ") + "\n"
        output_buffer += f"{e.path!r}, {e.message}\n"
        return str(output_buffer), 422

    return 'Validation OK', 200
