import sys


def get_detiled_error_message(error, error_details:sys):
    '''
    This function returns detailed error message
    
    Args:
        - error_message : str : Error message
        - error_details : str : Error details

    Returns:
        - str : Detailed error message
    '''
    _, _, tb = sys.exc_info()
    file_name = tb.tb_frame.f_code.co_filename
    line_no = tb.tb_lineno
    message = str(error)

    return f"An error occurred in {file_name} at line {line_no} with message {message} and details {error_details}"


class CustomException(Exception):
    '''
    Custom Exception class to handle exceptions
    '''
    def __init__(self, error_message, error_details:sys):
        '''
        Constructor for CustomException class

        Args:
            - error_message : str : Error message
            - error_details : str : Error details
        '''
        super().__init__(error_message)
        self.error_message = get_detiled_error_message(error_message, error_details=error_details)

    def __str__(self):
        '''
        This function returns the error message

        Returns:
            - str : Error message
        '''
        return self.error_message