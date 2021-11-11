# imports
import argparse
from server import Server
from client import Client
from util import input_key
import atexit


# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='Runs the server')
parser.add_argument('--client', action='store_true', help='Runs the client')
parser.add_argument('--server_host', type=str, default='', help='Host for the server')
parser.add_argument('--client_host', type=str, default='127.0.0.1', help='Host for the client')
parser.add_argument('--server_ip', type=str, default='127.0.0.1', help='IP address of the server')
parser.add_argument('--server_port', type=int, default=4000, help='Port at which server is running')
parser.add_argument('--client_port', type=int, default=4040, help='Port at which client is running')
parser.add_argument('--public', action='store_true', help='Allow access to your server without key')
parser.add_argument('--title', type=str, default='screen-share', help='The title of the window')

# parse the arguments
args = parser.parse_args()


# runs the server mode
def run_server():
	global args
	# create server instance
	server = Server(host=args.server_host, port=args.server_port, is_public=args.public)
	# connect the server and run
	if(server.connect()):
		server.run()


# runs the client mode
def run_client():
	global args
	# create the client
	client = Client(host=args.client_host, port=args.client_port)
	# connect to the server
	if(client.connect(server_ip=args.server_ip, server_port=args.server_port)):
		# get the key from the user
		user_key = input_key()
		# get the window title
		title = args.title
		# run the client
		try:
			# for successful termination close the client
			atexit.register(client.disconnect)
			# validate the key with the server
			client.validate_key_and_capture(key=user_key, title=title)
		except:
			# for any exception disconnect the client
			client.disconnect()





# invoke the functionality
if __name__ == '__main__':    
	# check the mode
	if args.server:
		# run in server mode
		print('Running server mode...')
		run_server()
	elif args.client:
		# run in client mode
		print('Running client mode...')
		run_client()
	else:
		# run in server mode
		print('No mode specified. Proceeding with default configurations.')
		print('Running server mode...')
		run_server()
