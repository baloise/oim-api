from oim_logging import get_oim_logger
from orchestra.OrchestraRequestHandler import OrchestraServiceInfoHandler
from zeep import helpers


def util_find_entry_in_list(list, keyname, expected_value):
    if not list or not keyname or type(list) is not list:
        return False
    for entry in list:
        try:
            if entry.get(keyname, None) == expected_value:
                return entry
        except KeyError:
            continue

    return False


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


def util_retrieve_services_by_name(pattern):
    log = get_oim_logger()
    serviceinfo = OrchestraServiceInfoHandler()
    results = serviceinfo.retrieveServicesByName(pattern=pattern)
    error = results.get('error', False)
    # log.debug(f'Error is {error} of type {type(error)}')
    if not results or error:
        # log.debug(f'Results is: {results}')
        log.error('retrieveServicesByName yielded error')
        return None
    if results.get('result', None):
        retval = util_strip_services_list(results.get('result', {}))
    return retval


def util_retrieve_person_by_id(id):
    log = get_oim_logger()
    serviceinfo = OrchestraServiceInfoHandler()
    results = serviceinfo.retrievePersonById(id=id)

    error = results.get('error', False)
    # log.debug(f'Error is {error} of type {type(error)}')
    if not results or error:
        # log.debug(f'Results is: {results}')
        log.error('retrievePersonById yielded error')
        return "Internal Server Error", 500

    person_entry = results.get('person_entry', {})
    person_entry = person_entry.get('Person', {})
    person_entry = person_entry[0] if type(person_entry) is list else person_entry
    return person_entry


def util_retrieve_responsibles_of_service(service_info, required_roles=['R']):
    log = get_oim_logger()

    result = {}

    if not service_info:
        return result

    service_name = service_info.get('servicename', '<unknown service name>')

    service_persons = service_info.get('ServicePerson', None)
    if not service_persons:
        log.warn(f'Could not retrieve ServicePerson for service {service_name}')
        return result

    for current_person in service_persons:
        # First we check if the person is even relevant (what role does he have in the service)
        is_considered = False
        for current_rr in current_person.get('ResponsibilityRole'):
            if current_rr.get('rolecode') in required_roles:
                is_considered = True
        if not is_considered:
            continue  # None of the the resproles match the required ones, NEEEEEEEEXT

        current_personid = current_person.get('personId', None)
        if not current_personid:
            log.warn(f'Error retrieving personId for one of the persons in service {service_name}!')
            continue  # skip to the next person
        # Lookup the person info...
        log.debug('Going to inspect person lookup now...')
        person_lookup = util_retrieve_person_by_id(id=current_personid)
        if not person_lookup:
            log.warn(f'Error looking up person info for personid {current_personid}!')
            continue  # skip to the next person
        current_username = person_lookup.get('persUserid', None)
        if not current_username:
            log.warn(f'Error looking up username for personid {current_personid}!')
            continue
        current_lastname = person_lookup.get('lastname', None)
        current_firstname = person_lookup.get('firstname', None)
        current_email = person_lookup.get('email', None)
        log.debug(f'Adding {current_username} to result set of responsible users')
        result[current_username] = {
            'lastname': current_lastname,
            'firstname': current_firstname,
            'email': current_email
        }

    return result


def post_orchestra_services_by_name(requestbody):
    log = get_oim_logger()
    pattern = requestbody['pattern']
    log.debug(f'Pattern is "{pattern}"')
    retval = util_retrieve_services_by_name(pattern=pattern)
    if not retval:
        return "Internal Server Error", 500
    return retval, 200


def get_orchestra_person_by_id(id):
    person_entry = util_retrieve_person_by_id(id=id)

    if not person_entry:
        return "Not Found", 404

    return person_entry, 200


def post_orchestra_responsibles_by_servicename(requestbody):
    log = get_oim_logger()
    service_name = requestbody['servicename']
    if not service_name:
        return "Bad request. (No servicename)", 400
    service_result = util_retrieve_services_by_name(pattern=service_name)
    if not service_result:
        return "Not found", 404
    # Reduce service results to first service if multiple were delivered
    log.debug(f'service_Resut is: {service_result}')
    if len(service_result) > 1:
        service_result = service_result[0]
    if type(service_result) is list:
        service_result = service_result[0]  # ugly unpacking, TODO prettify me

    responsibles = util_retrieve_responsibles_of_service(service_result)
    return responsibles, 200
