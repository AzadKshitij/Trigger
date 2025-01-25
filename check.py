# # Using print
# import logging


# def some_function_(x, y):
#     print('printing')
#     print(f"some_function called with args: {x}, {y}")
#     result = x + y
#     print(f"Result: {result}")
#     return result


# # Using logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# def some_function(x, y):
#     print('logger')
#     logger.debug(f"some_function called with args: {x}, {y}")
#     result = x + y
#     logger.info(f"Result: {result}")
#     return result


# some_function(1, 2)
# some_function_(1, 2)

# import logging

# # Create a logger
# logger = logging.getLogger('my_logger')
# logger.setLevel(logging.DEBUG)

# # Create a formatter to define the log format
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# # Create a file handler to write logs to a file
# file_handler = logging.FileHandler('app.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)

# # Create a stream handler to print logs to the console
# console_handler = logging.StreamHandler()
# # You can set the desired log level for console output
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)

# # Add the handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# # Now you can log messages with different levels
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')

import logging


class MyHandler(logging.Handler):

    def __init__(self, level=0):
        super().__init__(level)
        print(self.get_name())

    def emit(self, record):
        print('emited')
        # Do something with the log record
        # print(record.getMessage())
        print(record)


logger = logging.getLogger(__name__)
handler = MyHandler()
logger.addHandler(handler)

logger.info("This message will be processed by MyHandler.")
