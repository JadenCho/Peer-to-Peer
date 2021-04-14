###### Peer-to-Peer #####

This is our implementation of a basic Peer-to-Peer chat room.

How to use:
  Type in all parameters when prompted.
  When both users have entered all necessary info, that chat will begin.
  
How it works:
  Whenever a user types and sends a message, the other user will receive it.
  This is due to threading.
  Threading allows for real time chat interactions.
  Without threading, the messages would only update based on certain state changes such as when "enter" is pressed.
  
  Also, the messages are stored in SQLite3 databases.
  The sent messages are stored in chat_users_send.
  The received messages are stored in chat_users_recv.
  
  These 2 databases should hold the same messages given that both users are online.
  
  Please note that for the SQLite to work, the file path "C:\sqlite\db\" MUST exist.
  


