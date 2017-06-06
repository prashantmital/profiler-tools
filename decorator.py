from __future__ import division, print_function

from cProfile import Profile
from datetime import datetime
from functools import wraps
from os import getcwd, getpid, path


def profile_function(write_profile=True, profile_dir="{cwd}",
                     profile_name="{funcname}-{pid}-{timestamp}",
                     catch_exception=Exception):
    """
    Decorator that profiles the decorated function.

    Parameters
    ----------
    write_profile : bool
        Flag to instruct the decorator whether to write the profile to disk
        or not. If False, the profile is printed to STDOUT.
    profile_dir : str
        Python format string specifying the directory in which the profile
        file is created. The only supported special placeholder variable is
        `cwd` which expands to the current working directory. If the directory
        does not already exist, the profile will be printed to STDOUT and
        nothing will be written to disk.
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
    def profiling_decorator(func):
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
                write_dir = profile_dir.format(cwd=getcwd())
                if write_profile and path.isdir(write_dir):
                    write_name = "{}.prof".format(
                        profile_name.format(
                            funcname=func.__name__, pid=getpid(),
                            timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
                        ))
                    profile_path = path.join(write_dir, write_name)
                    profile.dump_stats(profile_path)
                else:
                    profile.print_stats()
            return result
        return profiled_func
    return profiling_decorator
