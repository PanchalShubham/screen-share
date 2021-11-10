# screen-share
A simple python program to share your screen with systems connected on same network.  

The program runs in two modes:  
- `server mode`: where your machine acts as a server and let other systems(clients) to see your screen live  
- `client mode`: where your machine acts a client and see server (machine running in server mode) live screen   

While running in `server mode` access to your machine is restricted via simple `key-matching` which you can avoid by runinng the server publicly.  

The following examples shows some samples to run the program:  
```bash
# run in server mode (by default key-protected)
# by default runs at 127.0.0.1 on port 4000
/home/user/screen-share$ python main.py --server  

# run in server mode without key protection
/home/user/screen-share$ python main.py --server --public

# run in server mode with your host and specific port
/home/user/screen-share$ python main.py --server --server_host 192.168.123.213 --server_port 4000


# run in client - by default runs at 127.0.0.1 on port 4040 and connects to server at 127.0.0.1 on port 4000
/home/user/screen-share$ python main.py --client  

# specify your host and port
/home/user/screen-share$ python main.py --client --client_host 192.168.132.214 --client_port 4040

# specify all details
/home/user/screen-share$ python main.py --client --client_host 192.168.132.214 --client_port 4040 --server_host 192.168.132.213 --server_port 4000


# you can specify the title of the window which might be helpful with multiple connections
/home/user/screen-share$ python main.py --client --title XYZ
 ```

 **NOTE:** This project is solely written for educational purposes and author is not responsible for any kind of misuse of this product. By using this product you agree to it.  
 