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
    name = "tpnotifier",
    author = "",
    author_email = "",
    version = "0.8",
    license = "GPL",
    description = "A text-based new-package notifier for ArchLinux without sudo",
    long_description = "README",
    url = "http://github.com/cdede/tpnotifier/",
    platforms = 'POSIX',
    packages = ['tpnoti' ],
    data_files = [
        (
            sysconfig.get_python_lib() + '/tpnoti',
            [
                './README'
            ]
        )
    ],
    scripts = ['tpnotifier', 'tpn_root']
)
