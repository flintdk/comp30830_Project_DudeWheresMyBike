# 22/03/01 TK; Don't think we need the following to activate conda v-env.
#          Have added a directive to Apache config instead...
#activate_this = '/home/ubuntu/miniconda3/envs/comp30830py39_dudeWMB/bin/?????activate?????'
#with open(activate_this) as f:
#	exec(f.read(:), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/dudeWMB/dudeWMB/")

from dudeWMB import dudeWMB as application

# If a factory function is used in a __init__.py file, then the function should be imported:
# from yourapplication import create_app
# application = create_app()