"""
    twtxt.parser
    ~~~~~~~~~~~~

    This module implements the parser for twtxt files.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import logging
from datetime import timezone
from itertools import islice

import dateutil.parser

from twtxt.types import Tweet

logger = logging.getLogger(__name__)


def make_aware(dt):
    """Appends tzinfo and assumes UTC, if datetime object has no tzinfo already."""
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def parse_iso8601(string):
    """Parse string using dateutil.parser."""
    return make_aware(dateutil.parser.parse(string))


def parse_string(string, source, limit=None):
    """Parses a multi-line string and returns extracted :class:`Tweet` objects."""
    tweets = []

    if limit:
        string = islice(string, limit)

    for line in string:
        try:
            parts = line.partition("\t")
            created_at = parse_iso8601(parts[0])
            text = parts[2].lstrip().rstrip()

            tweet = Tweet(text, created_at, source)
            tweets.append(tweet)

        except (ValueError, OverflowError) as e:
            logger.debug(e)

    return tweets
