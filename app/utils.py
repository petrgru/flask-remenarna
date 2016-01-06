from flask import flash, request, url_for



def flash_errors(form, category='danger'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                u'%s - %s' % (getattr(form, field).label.text, error),
                category
            )


def url_for_other_page(remove_args=[], **kwargs):
    args = request.args.copy()
    remove_args = ['_pjax']
    for key in remove_args:
        if key in args.keys():
            args.pop(key)
    new_args = [x for x in kwargs.iteritems()]
    for key, value in new_args:
        args[key] = value
    return url_for(request.endpoint, **args)


def timeago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

from random import randrange

def generate_12_random_numbers():
    numbers = []
    for x in range(12):
        numbers.append(randrange(10))
    return numbers

def calculate_checksum(ean):
    """
    Calculates the checksum for an EAN13
    @param list ean: List of 12 numbers for first part of EAN13
    :returns: The checksum for `ean`.
    :rtype: Integer
    """
    assert len(ean) == 12, "EAN must be a list of 12 numbers"
    sum_ = lambda x, y: int(x) + int(y)
    evensum = reduce(sum_, ean[::2])
    oddsum = reduce(sum_, ean[1::2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10

def ean13():
    numbers = generate_12_random_numbers()
    numbers.append(calculate_checksum(numbers))
    cislo = ''.join(map(str, numbers))
    return cislo

import argparse
import subprocess
import sys

from sqlalchemy.engine.url import make_url

def invoke_process(proc_name, proc_args, **subprocess_args):
    return subprocess.call([proc_name] + proc_args, **subprocess_args)

def parse_sqlalchemy_url(input_url):
    """
    Parses the input as a valid SQLAlchemy URL, or otherwise raises an
    exception that argparse will recognize as a type validation error.
    """
    try:
        url = make_url(input_url)
        _ = url.get_dialect()  # may throw if the URI refers to a mystery dialect
        return url
    except Exception as e:
        _, e, tb = sys.exc_info()
#        raise argparse.ArgumentTypeError, argparse.ArgumentTypeError(str(e)), tb