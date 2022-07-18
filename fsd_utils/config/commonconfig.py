import os
from pathlib import Path

class CommonConfig:

    # ---------------
    #  Application Config
    # ---------------
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "session_cookie")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    print("FLASK_ROOT:", FLASK_ROOT)