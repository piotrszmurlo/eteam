from fastapi import Request


def call_api_gateway(request: Request):
    service_id = request.path_params['service_id']
    print(request.path_params)
    if service_id == str(1) or service_id =='storage':
        raise RedirectStorageServiceException()
    elif service_id == str(2):
        raise RedirectNotificationPortalException()
    elif service_id == str(3):
        raise RedirectLibraryPortalException()


class RedirectStorageServiceException(Exception):
    pass


class RedirectNotificationPortalException(Exception):
    pass


class RedirectLibraryPortalException(Exception):
    pass