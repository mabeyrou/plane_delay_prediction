import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# def pytest_configure():
#     load_dotenv(dotenv_path=".env.test")
