import logging

if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr.
    # If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(
        level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]\t%(message)s"
    )
