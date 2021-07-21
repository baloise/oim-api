import unittest
import flask_unittest
from app import create_flask_app
import re
from unittest import mock
from dotenv import load_dotenv
from tests.ocRequestGeneration_test import TestOcRequestJson  # noqa: F401

# Force overwrite envvars with mock values from .env.unittests
load_dotenv(dotenv_path='.env', override=False)


if __name__ == '__main__':
    unittest.main()
