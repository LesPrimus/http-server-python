def get_headers(*args) -> dict:
    return dict([tuple(arg.split(":", 1)) for arg in args if arg])  # noqa
