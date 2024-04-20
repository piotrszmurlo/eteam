from fastapi import Request


def call_api_gateway(request: Request):
    service_id = request.path_params['service_id']
    print(request.path_params)
    if service_id == str(1):
        raise RedirectAuthServiceException()
    elif service_id == str(2):
        raise RedirectStorageServiceException()
    elif service_id == str(3):
        raise RedirectNotificationServiceException()


class RedirectAuthServiceException(Exception):
    pass


class RedirectStorageServiceException(Exception):
    pass


class RedirectNotificationServiceException(Exception):
    pass