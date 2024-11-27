import sys
from datetime import datetime
import os
import json
import shutil
from crontab import CronTab

logic_implementation = sys.argv[1]

# Create folder
path = os.path.join('logs', datetime.now().strftime('%Y-%m-%dT%H-%M'))
if not os.path.exists(path):
    os.makedirs(path)

# Copy and rename logic implementation
destination_path = os.path.join('strategy', 'DefenceStrategyImplementation.py')
if os.path.abspath(logic_implementation) != os.path.abspath(destination_path):
    shutil.copyfile(logic_implementation, destination_path)

shutil.copyfile(logic_implementation, os.path.join(path, 'DefenceStrategyImplementation.py'))

# Create Cron job
cron = CronTab(user=True)
command = f'python3 {os.path.dirname(os.path.realpath(__file__))}/respond.py {path} >> {os.path.dirname(os.path.realpath(__file__))}/debug 2>&1'
job = cron.new(command=command, comment='strategy evaluation')
job.minute.every(1)
cron.write()

# Note beginning
with open(os.path.join(path, 'info'), 'w+') as info:
    info.write(json.dumps({"start": datetime.utcnow().isoformat()}) + "\n")
