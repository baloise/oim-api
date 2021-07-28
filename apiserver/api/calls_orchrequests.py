from oim_logging import get_oim_logger
from orchestra.OrchestraRequestHandler import OrchestraServiceInfoHandler
from pprint import pformat


def util_strip_services_list(services={},
                             keys_to_keep=[
                                 'servicename',
                                 'servicesId',
                                 'servicesNo',
                                 'servicetypeId',
                                 'ServicePerson'
                             ]):
    if (not type(keys_to_keep) is list) or len(keys_to_keep) < 1:
        return services

    output = []

    for current_service in services.get('Services', {}):
        build_service = {}
        for current_key in current_service:
            current_value = current_service.get(current_key, None)
            if current_key in keys_to_keep:
                # if current_key == 'ServicePerson':
                #     current_value = util_strip_serviceperson(person=current_value)
                build_service[current_key] = current_value
        output.append(build_service)

    return output


def post_orchestra_services_by_name(requestbody):
    log = get_oim_logger()
    pattern = requestbody['pattern']
    log.debug(f'Pattern is "{pattern}"')
    serviceinfo = OrchestraServiceInfoHandler()
    results = serviceinfo.retrieveServicesByName(pattern=pattern)
    if not results or results.get('error', False) is False:
        log.error('retrieveServicesByName yielded error')
        return "Internal Server Error", 500
    if results.get('result', None):
        retval = util_strip_services_list(results.get('result', {}))

    # log.debug(f'Results: {pformat(retval)}')
    return retval, 200


def get_orchestra_person_by_id(id):
    log = get_oim_logger()
    serviceinfo = OrchestraServiceInfoHandler()
    results = serviceinfo.retrievePersonById(id=id)

    if not results or results.get('error', True) is True:
        log.error('retrievePersonById yielded error')
        return "Internal Server Error", 500

    person_entry = results.get('person_entry', {})
    person_entry = person_entry.get('Person', {})
    person_entry = person_entry[0] if type(person_entry) is list else person_entry
    if not person_entry:
        return "Not Found", 404

    return person_entry, 200
