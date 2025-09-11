import os, logging, datetime, sys

def setup_logging(module_name=None):
    """
    Configure and return a logger for the specified module.
    
    Args:
        module_name (str, optional): The name to use for the logger. Defaults to the caller's module name.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Set up logging
    log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, f'app_{datetime.datetime.now().strftime("%Y%m%d")}.log')

    # Use provided module name or caller's module name
    logger_name = module_name if module_name else 'monitoring_app'
    logger = logging.getLogger(logger_name)
    
    # Only add handlers if they haven't been added already
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file)
        cons_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        cons_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(cons_handler)
    
    return logger