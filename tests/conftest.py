# """
# Contains test configuration.
# """
# import os

# import pytest
# from config import Config
# from core.app import create_app

# @pytest.fixture(scope="function")
# def flask_test_client():
#     """
#     Creates the test client we will be using to test the responses
#     from our app, this is a test fixture.
#     :return: A flask test client.
#     """

#     with create_app().app_context() as app_context:
#         with app_context.app.test_client() as test_client:
#             yield test_client
pass