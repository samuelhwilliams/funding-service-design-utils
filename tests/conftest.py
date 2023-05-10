"""
Contains test configuration.
"""
from pathlib import Path

import pytest
from flask import Flask
from flask import g
from fsd_utils.authentication.decorators import login_requested
from fsd_utils.authentication.decorators import login_required


def create_app():
    app = Flask("test")
    return app


@pytest.fixture(scope="function")
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().app_context() as app_context:
        _test_public_key_path = str(Path(__file__).parent) + "/keys/rsa256/public.pem"
        with open(_test_public_key_path, mode="rb") as public_key_file:
            rsa256_public_key = public_key_file.read()

        app_context.app.config.update(
            {
                "FSD_LANG_COOKIE_NAME": "language",
                "COOKIE_DOMAIN": None,
                "FSD_USER_TOKEN_COOKIE_NAME": "fsd-user-token",
                "AUTHENTICATOR_HOST": "https://authenticator",
                "RSA256_PUBLIC_KEY": rsa256_public_key,
            }
        )
        app_context.app.add_url_rule(
            "/mock_login_required_route",
            "mock_login_required_route",
            mock_login_required_route,
        )
        app_context.app.add_url_rule(
            "/mock_login_requested_route",
            "mock_login_requested_route",
            mock_login_requested_route,
        )
        app_context.app.add_url_rule(
            "/mock_login_required_roles_route",
            "mock_login_required_roles_route",
            mock_login_required_roles_route,
        )
        app_context.app.add_url_rule(
            "/mock_login_required_admin_roles_route",
            "mock_login_required_admin_roles_route",
            mock_login_required_admin_roles_route,
        )
        with app_context.app.test_client() as test_client:
            yield test_client


@pytest.fixture(scope="function")
def flask_test_development_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().app_context() as app_context:
        _test_public_key_path = str(Path(__file__).parent) + "/keys/rsa256/public.pem"
        with open(_test_public_key_path, mode="rb") as public_key_file:
            rsa256_public_key = public_key_file.read()

        app_context.app.config.update(
            {
                "FSD_LANG_COOKIE_NAME": "language",
                "COOKIE_DOMAIN": None,
                "FLASK_ENV": "development",
                "DEBUG_USER_ROLE": "ADMIN",
                "DEBUG_USER": {
                    "full_name": "Development User",
                    "email": "dev@example.com",
                    "roles": ["ADMIN", "TEST"],
                    "highest_role": "ADMIN",
                },
                "FSD_USER_TOKEN_COOKIE_NAME": "fsd-user-token",
                "AUTHENTICATOR_HOST": "https://authenticator",
                "RSA256_PUBLIC_KEY": rsa256_public_key,
            }
        )
        app_context.app.add_url_rule(
            "/mock_login_required_roles_route",
            "mock_login_required_roles_route",
            mock_login_required_roles_route,
        )
        app_context.app.add_url_rule(
            "/mock_login_required_admin_roles_route",
            "mock_login_required_admin_roles_route",
            mock_login_required_admin_roles_route,
        )
        with app_context.app.test_client() as test_client:
            yield test_client


@login_required
def mock_login_required_route():
    """
    A mock route function decorated with @login_required
    Here we expect a non logged in user to be redirected
    to authenticator, and a logged in user to have the required
    Flask request g variables set as below:
    g: {
        "is_authenticated": True,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": "test-user",
        "user": User(
            email="test@example.com",
            full_name="Test User",
            highest_role="LEAD_ASSESSOR",
            roles=["LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"]
        )
    :return: the Flask g variable serialised as a dict/json
    """
    return vars(g)


@login_requested
def mock_login_requested_route():
    """
    A mock route function decorated with @login_requested
    Here we expect a logged in user to have the required
    Flask request g variables set as below:
    g: {
        "is_authenticated": True,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": "test-user",
        "user": User(
            email="test@example.com",
            full_name="Test User",
            highest_role="LEAD_ASSESSOR",
            roles=["LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"]
        )
    and a non logged in user to have the Flask request g variables
    set as below:
    g: {
        "is_authenticated": False,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": None,
    }
    :return: the Flask g variable serialised as a dict/json
    """
    return vars(g)


@login_required(roles_required=["COMMENTER"])
def mock_login_required_roles_route():
    """
    A mock route function decorated with
    @login_required(roles_required=["COMMENTER"])
    Here we expect a logged in user without the "COMMENTER"
    role to be redirected to a missing roles required
    error page on authenticator,
    and a logged in user WITH the "COMMENTER" role
    to have the required
    Flask request g variables set as below:
    g: {
        "is_authenticated": True,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": "test-user",
        "user": User(
            email="test@example.com",
            full_name="Test User",
            highest_role="LEAD_ASSESSOR",
            roles=["LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"]
        )
    :return: the Flask g variable serialised as a dict/json
    """
    return vars(g)


@login_required(roles_required=["ADMIN", "TEST"])
def mock_login_required_admin_roles_route():
    """
    A mock route function decorated with
    @login_required(roles_required=["ADMIN","TEST"])
    Here we expect a logged in user without the "ADMIN","TEST"
    role to be redirected to a missing roles required
    error page on authenticator,
    and a logged in user WITH BOTH the "ADMIN" and "TEST" roles
    to have the required
    Flask request g variables set as below:
    g: {
        "is_authenticated": True,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": "test-user",
        "user": User(
            email="test@example.com",
            full_name="Test User",
            highest_role="LEAD_ASSESSOR",
            roles=["LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"]
        )
    :return: the Flask g variable serialised as a dict/json
    """
    return vars(g)
