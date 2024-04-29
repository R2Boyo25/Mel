def strtobool(val: str | bool) -> bool:
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', 'ye', 'yep', 'yeah', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', 'nope', and '0'.  Raises ValueError if
    'val' is anything else.
    """

    if type(val) is bool:
        return val

    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "ye", "yep", "yeah", "1"):
        return True

    elif val in ("n", "no", "f", "false", "off", "nope", "0"):
        return False

    else:
        raise ValueError(
            f"I don't know what '{val}' means when interpreted as yes or no."
        )
