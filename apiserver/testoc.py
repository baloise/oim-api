import unittest
from app import create_flask_app
from dotenv import load_dotenv
from tests.ocRequestGeneration_test import TestOcRequestJson  # noqa: F401

# Force overwrite envvars with mock values from .env.unittests
load_dotenv(dotenv_path='.env', override=False)

test_db_order = TestOcRequestJson()

if __name__ == '__main__':
    unittest.main()
