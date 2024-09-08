import logging

def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s    [%(asctime)s]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    return logging.getLogger(name)