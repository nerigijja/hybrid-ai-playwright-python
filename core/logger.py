from loguru import logger
import sys, pathlib

def init_logger(artifacts_dir: pathlib.Path):
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    logfile = artifacts_dir / "run.log"
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    logger.add(logfile, level="DEBUG", rotation="1 MB", retention=5)
    return logger
