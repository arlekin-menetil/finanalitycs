def log(msg):

    msg = str(msg)

    if any(
        x in msg
        for x in [
            "SHORT INFO",
            "SHORT INFO DICT",
            "DEBUG STRUCTURED",
            "CURRENCY FOUND",
            "AMOUNT MIN",
            "AMOUNT MAX",
            "description parsed",
        ]
    ):
        return

    print(f"[BANK.UZ] {msg}")