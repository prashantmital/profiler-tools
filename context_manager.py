import cProfile
import contextlib
import datetime


@contextlib.contextmanager
def profile(write_profile=False, profile_name="pyprofile-{timestamp}"):
    profile = cProfile.Profile()
    try:
        profile.enable()
        yield
        profile.disable()
    finally:
        if write_profile:
            profile.dump_stats("{}.prof".format(profile_name.format(
                timestamp=str(datetime.datetime.now()).replace(' ', '_')
            )))
        profile.print_stats()
