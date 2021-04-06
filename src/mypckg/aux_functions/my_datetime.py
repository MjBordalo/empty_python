'''Python'''
from datetime import datetime
from datetime import date
from datetime import time
'''
Conventions used:
%d  Day of the month as a zero-padded decimal number.	01, 02, ..., 31
%m	Month as a zero-padded decimal number.	01, 02, ..., 12
%Y	Year with century as a decimal number.	0001, 0002, ..., 2013, 2014
%H	Hour (24-hour clock) as a zero-padded decimal number.	00, 01, ..., 23
%M	Minute as a zero-padded decimal number.	00, 01, ..., 59
%S	Second as a zero-padded decimal number.	00, 01, ..., 59
'''

def try_parsing_time_or_datetime(text):
    if isinstance(text, time) or isinstance(text, datetime):
        return text
    for fmt in ('%H:%M:%S', '%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
        try:
            if fmt == '%H:%M:%S' or fmt == '%H:%M':
                return datetime.strptime(text, fmt).time()
            else:
                return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def try_parsing_time(text):
    if isinstance(text, time):
        return text
    for fmt in ('%H:%M:%S', '%H:%M'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def try_parsing_date(text):
    if isinstance(text, date):
        return text
    for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def try_parsing_datetime(text):
    if isinstance(text, datetime):
        return text
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')
