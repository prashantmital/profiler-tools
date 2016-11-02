import cProfile
import datetime


def profile(write_profile=False, profile_name="{funcname}-{timestamp}"):
    def profiled_func_decorator(func):
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
            finally:
                if write_profile:
                    profile.dump_stats("{}.prof".format(profile_name.format(
                        funcname=func.__name__,
                        timestamp=str(datetime.datetime.now()).replace(' ', '_')
                    )))
                profile.print_stats()
                return result
        return profiled_func
    return profiled_func_decorator
