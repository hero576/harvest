# parse google auth from app
# https://github.com/krissrex/google-authenticator-exporter.git　


import base64
import sys

import googleauth_pb2
from urllib.parse import unquote, urlparse


def get_data(data):
    return unquote(urlparse(data).query.split("=")[1])


def get_ga_code(data):
    binary_data = base64.b64decode(data)
    p = googleauth_pb2.MigrationPayload()
    p.ParseFromString(binary_data)
    # print(p)
    for i in p.otp_parameters:
        secret = base64.b32encode(i.secret).decode()
        print(f"auth-{i.name}: {secret}")


if __name__ == '__main__':
    if len(sys.argv)<1:
        print("Usage: need a otpauth content, example: tpauth-migration://offline?data=xxxx")
    else:
        auth_url = sys.argv[1]
        get_ga_code(get_data(auth_url))
