from loguru import logger
from rich.logging import RichHandler
from pyinspect import install_traceback

install_traceback()

logger.configure(
    handlers=[{"sink": RichHandler(markup=True), "format": "{message}"}]
)

from rich.pretty import install

install()


from kino import animal
from kino import geometry
