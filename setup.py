import sys

from distutils import sysconfig
from distutils.core import setup

try:
    import feedparser
except:
    print ('')
    print ('tpnotifier requires the python-feedparser')
    sys.exit(0)

setup(
    name = "tcgmail",
    author = "",
    author_email = "",
    version = "0.8",
    license = "GPL",
    description = "A text-based notifier for gmail",
    long_description = "README",
    url = "http://github.com/cdede/tcgmail/",
    platforms = 'POSIX',
    packages = ['tcgmail' ],
    data_files = [
        (
            sysconfig.get_python_lib() + '/tcgmail',
            [
                './README'
            ]
        )
    ],
    scripts = ['tcgmai']
)
