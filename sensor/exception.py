import sys,os

def error_message_detail(error, error_detail: sys):     #error_detail gives details about the error using sys module 
    _, _, exc_tb = error_detail.exc_info()  #exc_tb gives the line number where the error occurred also exc_info() returns 3 values ( _, _, exc_tb)
    #
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(     #[{0}] coz filename is placed at 0th index 
        #[{1}] coz exc_tb.tb_lineno is placed at 1st index and [{2}] coz str(error) is placed at 2nd index 
        file_name, exc_tb.tb_lineno, str(error)     #file_name gives the name of the file where the error occurred
    )
    return error_message



class SensorException(Exception):   #(Exception) this is inherited from Exception class

    def __init__(self,error_message, error_detail:sys):
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message



