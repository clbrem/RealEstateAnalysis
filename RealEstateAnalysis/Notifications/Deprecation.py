import warnings

def deprecateNotification(name, version):
    if version is not None:
        warning = "Method {0} will be deprecated in version {1}".format(name, version)
    else:
        warning = "Method {0} will be deprecated in an upcoming version".format(name)
    warnings.warn(warning, DeprecationWarning, stacklevel=2)

    

def deprecated(name, version = None):
    def deprecate(f):
        def inner(*args, **kwargs):
            deprecateNotification(name, version)
            return f(*args, **kwargs)
        return inner
    return deprecate
