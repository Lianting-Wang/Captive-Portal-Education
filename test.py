import time
import shutil
import threading
import subprocess
from answer.server import Server
from test_mininet import test_mininet

# server = Server()
# Server_thread = threading.Thread(target=server.run_tcp_server)
# Server_thread.start()

# pox_source_file = './pox_answer/condition_switch_answer.py'
# pox_tcp_source_file = './pox_answer/TCPClient.py'
# destination_directory = '/home/mininet/pox/ext'

# shutil.copy(pox_source_file, destination_directory)
# shutil.copy(pox_tcp_source_file, destination_directory)

# process =  subprocess.Popen(["sudo", "/home/mininet/pox/pox.py", "condition_switch_answer"])

test_mininet(0)

with open('mininet_grade.txt', 'r') as file:
    print(file.read())


# server.stop_server()
# server_thread.join()
# process.terminate()
# process.wait()