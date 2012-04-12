import os
import sys

import transaction
from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pp.common.db import dbsetup

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    dbsetup.setup(dbsetup.modules_from_config(settings, 'commondb.'))
    dbsetup.init_from_config(settings, 'sqlalchemy.')
    with transaction.manager:
        dbsetup.create()
