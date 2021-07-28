from zeep.xsd.types.collection import ListType
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


def get_orchestra_services_by_name(requestbody):
    log = get_oim_logger()
    pattern = requestbody['pattern']
    log.debug(f'Pattern is "{pattern}"')
    serviceinfo = OrchestraServiceInfoHandler()
    results = serviceinfo.retrieveServicesByName(pattern=pattern)
    if results and results.get('result', None) and results.get('error', False) is False:
        retval = util_strip_services_list(results.get('result', {}))
    # log.debug(f'Results: {pformat(retval)}')
    return retval, 200


def get_orchestra_person_by_id(person_id):
    log = get_oim_logger()
    serviceinfo = OrchestraServiceInfoHandler()
    results = serviceinfo.retrievePersonById(person_id=person_id)
    log.debug(f'Results: {pformat(results)}')
    return results, 200
