from cProfile import Profile
from datetime import datetime
from functools import wraps


def profile(write_profile=False, profile_name="{funcname}-{timestamp}",
            catch_exception=Exception):
    """
    Decorator that profiles the decorated function.

    Parameters
    ----------
    write_profile : bool
        Flag to instruct the decorator whether to write the profile to disk
        or not. If False, the profile is printed to STDOUT.
    profile_name : str
        Python format string specifying the name of the file to which the
        profile is written. Supported special placeholder variables are
        `funcname` (yields the decorated function's name) and `timestamp`.
        The full filename is appended with a .prof extension before being
        written to disk.
    catch_exception : Exception
        Specify exception type to be handled appropriately if encountered
        during profiling. All exceptions subclassed from `catch_exception` will
        be handled appropriately during profiling. By default we handle all
        exceptions appropriately, but this argument can be used to narrow
        that down. If an exception that is not subclassed from
        `catch_exception` is raised, execution will terminate prematurely
        and no profile will be generated.
    """
    def profiled_func_decorator(func):
        @wraps(func)
        def profiled_func(*args, **kwargs):
            profile = Profile()
            result = None
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
            except catch_exception as exc:
                result = exc
            finally:
                if write_profile:
                    profile.dump_stats("{}.prof".format(profile_name.format(
                        funcname=func.__name__,
                        timestamp=datetime.now().strftime("%Y%m%d_%H%M%S%f")
                    )))
                else:
                    profile.print_stats()
                if issubclass(result, catch_exception):
                    raise result
                else:
                    return result
        return profiled_func
    return profiled_func_decorator
