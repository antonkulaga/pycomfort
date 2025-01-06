import sys
from enum import Enum
from typing import Union
import warnings

import dotenv
from dotenv import load_dotenv
import os
from deprecated import deprecated

from pycomfort.logging import LogLevel

try:
    from loguru import logger
    HAS_LOGURU = True
except ImportError:
    HAS_LOGURU = False



LOG_LEVELS = [loader.value for loader in LogLevel]

@deprecated(
    reason="Please configure loguru directly in your application. We will remove this in future versions",
    version='0.0.17'
)
def configure_logger(log_level: Union[str, LogLevel], add_stdout: bool = False):
    """Configure loguru logger with specified log level and stdout options
    
    Args:
        log_level: Either a LogLevel enum or string matching a log level
        add_stdout: If True, adds stdout as a log sink
    
    Returns:
        Configured logger instance
    
    Raises:
        ImportError: If loguru package is not installed
    """
    if not HAS_LOGURU:
        raise ImportError("loguru is required for configure_logger but it is not installed. "
                        "Install it with: pip install loguru")
    
    level = log_level.value if isinstance(log_level, LogLevel) else log_level
    if level.upper() != LogLevel.NONE.value and add_stdout:
        logger.add(sys.stdout, level=level.upper())
    return logger


def load_environment_keys(debug: bool = True, usecwd: bool = False):
    """Load OpenAI API key from .env file
    
    Args:
        debug: If True, prints debug information about env file location
        usecwd: If True, searches for .env file in current working directory
               If False, searches in parent directories
    
    Returns:
        str: OpenAI API key if found, None otherwise
    """
    # Find .env file location
    e = dotenv.find_dotenv(usecwd=usecwd)
    print(e)
    if debug:
        print(f"environment found at {e}")
    
    # Load environment variables from .env file
    has_env: bool = load_dotenv(e, verbose=True, override=True)
    if not has_env:
        print("Did not found environment file, using system OpenAI key (if exists)")
    
    # Get OpenAI key from environment variables
    openai_key = os.getenv('OPENAI_API_KEY')
    return openai_key