import json
import os
from crontab import CronTab
from datetime import datetime

dirs = sorted([name for name in os.listdir('logs') if os.path.isdir(os.path.join('logs', name))], reverse=True)
dir = dirs[0]

# Remove cron job
cron = CronTab(user=True)
cron.remove_all(comment="strategy evaluation")
cron.write()

# Note end
info_file = os.path.join('logs', dir, 'info')
info = json.loads(open(info_file, 'r').read())
info["end"] = datetime.utcnow().isoformat()
with open(info_file, 'w') as f:
    f.write(json.dumps(info) + "\n")
