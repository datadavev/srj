import subprocess
import sys
import platform
import pkg_resources
import sysconfig
import json
import sqlite3
from flask import Flask, Response

'''
amazon-linux-extras install python3.8;mkdir /var/task/public; ls -la; pip3 install -r requirements.txt
'''

app = Flask(__name__)


def system_call(command):
    """
    params:
        command: list of strings, ex. `["ls", "-l"]`
    returns: output, success
    """
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
        success = True
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        success = False
    return output, success


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    j = "\n"
    msg = []
    msg.append(platform.platform())
    msg.append(f"python {sys.version_info.major}.{sys.version_info.minor}")
    msg.append(f"{j.join(sys.path)}")
    msg.append("---")
    _paths = sysconfig.get_paths()
    msg.append(f"{json.dumps(_paths, indent=2)}")
    msg.append("---")
    output, success = system_call(["ls", "-l", "/var/lang/lib/python3.6"])
    msg.append(output)
    msg.append("---pwd:")
    output, success = system_call(["pwd", ])
    msg.append(output)
    msg.append("---")
    output, success = system_call(["ls", "-l", "api"])
    msg.append(output)
    output,success = system_call(["sqlite3", "--version"])
    msg.append(output)
    output,success = system_call(["which", "python"])
    msg.append(output)

    msg += {d.project_name: d.version for d in pkg_resources.working_set}
    return Response(f"<pre>{j.join(msg)}</pre>", mimetype="text/html")
