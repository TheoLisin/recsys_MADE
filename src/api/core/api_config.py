import sys
from dotenv import load_dotenv
from os import environ

load_dotenv()

API_V1_STR: str = "/api"
JWT_SECRET: str = environ.get("JWT_SECRET") or "TEST_SECRET_DO_NOT_USE_IN_PROD"
ALGORITHM: str = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

token_exp = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

if token_exp is not None and token_exp.isnumeric():
    ACCESS_TOKEN_EXPIRE_MINUTES = int(token_exp)
else:
    sys.stderr.write(
        "ACCESS_TOKEN_EXPIRE_MINUTES is not specified or is not in a valid format. Set to default: 8 days.\n",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 8 days
