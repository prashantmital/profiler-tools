import cProfile
import datetime


def profile(write_profile=False, profile_name="{funcname}-{timestamp}",
            catch_exception=Exception):
    def profiled_func_decorator(func):
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
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
                        timestamp=str(datetime.datetime.now()).replace(' ', '_')
                    )))
                profile.print_stats()
                if isinstance(result, catch_exception):
                    raise result
                else:
                    return result
        return profiled_func
    return profiled_func_decorator
