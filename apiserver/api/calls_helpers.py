from models.orders import Person, SbuType
from oim_logging import get_oim_logger
from app import db
import random
import string


def persist_person(email):
    logger = get_oim_logger()
    aPerson = Person.query.filter_by(email=email).first()
    if aPerson is None:
        random_name = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
        logger.debug(f"Create person: {email} ({random_name})")
        newPerson = Person(
            username=random_name,  # fetch username from AD
            email=email,
            sbu=SbuType.SHARED  # fetch sbu from AD
        )
        db.session.add(newPerson)
        db.session.commit()
        aPerson = newPerson
    else:
        logger.debug("Person already exists: {}".format(email))
    return aPerson
