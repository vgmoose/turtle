:turtle:

**turtle** is a chat client/server that aims to be a quick way to connect users that are within a shell. They can be within the same machine or on separate ones

#### usage
```
python client.py [IP address] [port]
```

#### example
##### Over the network
User A: (on 192.168.1.106)
```
$ python cilent.py
nobody's here yet...
```
User B:
```
$ python client.py 192.168.1.106
connected to 1 user
```
At this point, User A and User B can now talk by typing and hitting enter to send. If one of them wants, they can run /shell or /exec (see below) to run commands while they chat.

##### On the same machine
Communication can also be established between two users on the same machine, locally. This can create an interesting workflow where both users ssh into a shared machine/cloud server, and then run turtle to talk securely. The end result is something similar to [ssh-chat](https://github.com/shazow/ssh-chat), but with no setup on the server.

Both users can run:
```
python client.py
```
It will default to localhost, so no matter where the users are physically located, if they are running the command on the same machine they will be connected.

#### design
turtle is designed with the philosophy that all users are clients, and nobody should explicitly have to designate themselves a "server". Ideally the program would "just work" between two clients that run it.

It achieves this by, if no target hosts/IPs have been specified, transparently becoming the host. Then upon disconnecting would delegate to a connected client the job of being host.

##### Notes
- default port is 55225
- if no IP is specified, your IP will be the chatroom
- if an IP is specified, but there is no one hosting on it, your IP will be the chatroom

#### commands
- /nick [newname]
- /leave
- /clear
- /buzz
- /exec [command] (eg. "/exec bash") for shell+chat

#### todo
- more than two people
- direct connect without port forwarding(?)
- "chaining" of IP addresses (failover)
- tighter shell integration
- compatibility with [cciollaro's chat](https://github.com/cciollaro/chat)
- fingerprint verification / OTR / password
- localhost only mode
- ssl for sockets
