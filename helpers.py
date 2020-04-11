import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def compare_list(list1, list2):
    intersection = len(list(set(list1).intersection(set(list2))))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
