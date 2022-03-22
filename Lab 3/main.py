import ui2, server, os
from threading import Thread


os.system('rm heat.txt light.txt')
os.system('touch heat.txt light.txt')
# start server
server_thread = Thread(target=server.start_server, daemon=True)
server_thread.start()

# start ui
try:
	ui2.run_ui()
except:
	os.system('rm heat.txt light.txt')



