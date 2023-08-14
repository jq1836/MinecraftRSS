import time

'''
Prints the local time.
'''
class _Clock:
    
    def getTime(self) -> str:
        currTime = time.localtime()
        return f'=== {currTime.tm_mday}/{currTime.tm_mon}/{currTime.tm_year} '\
              + f'at {currTime.tm_hour}:{currTime.tm_min}:{currTime.tm_sec} ==='

clock = _Clock()
