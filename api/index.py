import subprocess
import sys
import platform
from http.server import BaseHTTPRequestHandler
import pkg_resources
import sysconfig
import json
import sqlite3


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


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
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
        msg.append("---")
        output, success = system_call(["yum", "list"])
        msg.append(output)
        msg.append("---")
        output, success = system_call(["ls", "-l"])
        msg.append(output)
        output,success = system_call(["sqlite3", "--version"])
        msg.append(output)
        output,success = system_call(["which", "python"])
        msg.append(output)

        msg += {d.project_name: d.version for d in pkg_resources.working_set}
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"<pre>{j.join(msg)}</pre>".encode())
