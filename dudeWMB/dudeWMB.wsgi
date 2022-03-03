/home/ubuntu/miniconda3/envs/comp30830py39_dudeWMB/bin/dwmb_dl??????

activate_this = '/home/ubuntu/src/dudeWMB/venv/bin/activate_this.py'
with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/dudeWMB/")

from app import app as application