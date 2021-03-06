import sys

from distutils import sysconfig
from distutils.core import setup

try:
    import os
except:
    print ('')
    sys.exit(0)

setup(
    name = "tcgmail",
    author = "",
    author_email = "",
    version = "1.0.23",
    license = "GPL3",
    description = "A text-based notifier for gmail",
    long_description = "README",
    url = "http://github.com/cdede/tcgmail/",
    platforms = 'POSIX',
    packages = ['libtcg' ],
    data_files = [  ('share/doc/tcgmail', ['README', 'COPYING']),
        ('share/tcgmail',['example_config']) ,
    ],
    scripts = ['tcgmail']
)
