#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.auth import Auth

    a = Auth()
    path = "/api/v1/uas"
    paths_excluded = ["/api/v1/us*"]
    res = a.require_auth(path, paths_excluded)
    print(res)
    if not res:
        print("require_auth must return False: {} - {}".format(path, paths_excluded))
        exit(1)
    print("OK", end="")
    