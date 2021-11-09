# imports
import argparse
from server import Server
from client import Client


# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='Runs the server')
parser.add_argument('--client', action='store_true', help='Runs the client')
parser.add_argument('--server_host', type=str, default='')
parser.add_argument('--client_host', type=str, default='127.0.0.1')
parser.add_argument('--server_ip', type=str, default='127.0.0.1')
parser.add_argument('--server_port', type=int, default=4000)
parser.add_argument('--client_port', type=int, default=4040)

# parse the arguments
args = parser.parse_args()


# runs the server mode
def run_server():
    global args
    # create server instance
    server = Server(host=args.server_host, port=args.server_port)
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
		if(client.handshake()):
			client.capture_server_screen()
			user_inp = ''
			while user_inp != 'quit':
				user_inp = input('>> ')
				print(user_inp)
				if (user_inp == 'stop capture'):
					client.stop_capturing_server_screen()
				elif (user_inp == 'exit'):
					client.stop_capturing_server_screen()
				break
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
