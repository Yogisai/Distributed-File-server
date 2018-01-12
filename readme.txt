---------------------------PA4---------------------------

	DISTRIBUTED FILE SERVER

---------------------------------------------------------

SERVERS:

4 servers are written in  similar fashion.

Each server runs on a different port.

3 Basic Functionalities
 ------------------------------------ 
1. Put: 
Authentication is done first by receiving the credentials from the client.

Only if the username and password match as in dfs config file , the operation continues

If authentication fails after 5 tries, the server closes the connection to the client.

The files come divided and 2 parts to each distributed server.

The division is based on the MD5 value of the total file.

These parts are stored with an extension depending on the part number.

The MD5 value is recieved first and the server then recieves and makes the file names according to the MD5 value.

These files are written in a directory named as the username of the person logging in and under another subdirectory as the file name.

------------------------------------------
2. Get:

Similar to put this authenticates the user before proceeding.

After authentication, the server proceeds to the respective directory and sends the calculated MD5 value to the client.

Then it proceeds to send all the files one by one in the folder with the folder name as username.

The rest, joining and optimization is handled at the client.

-------------------------------------
3. List

Again, the server authenticates before sending the filenames like above.

After authentication, the server sends all the filenames to the client followed by done indicating that all the filenames have been sent.

Checking is done at the client end.

-------------------------------------------------------------------
-------------------------------------------------------------------
CLIENT:

The client is where most of the work is done.
Everytime the client is started, it requests authentication.

After authentication, it try to connect to all the 4 servers

Everytime a request is made, it requests authentication

If a valid request is made, the required function is called.

The client handles 4 basic functionalities.

---------------------------------------------
1. Put:

When the put command is given, the client first authenticates.
5 tries are given after which the client closes.

if authentication is done, client checks if the file is present.

If the file is available, it is opened, read and md5 value is taken.

Depending on the value, the file is divided into 4 equal parts and sent to each server to be kept.

before sending the files, the client also sends the md5 value and credentials for the server to accept.

-------------------------------------------------------
2.Get

again the credentials are checked both on client and server side.

Once get fucntion is called, it requests each server to send the files it has.

For optimization, it first checks servers 1 and 3.

if all the 4 files are recieved, it combines them and makes the file.

if all of them are not recieved, it checks further in server 2 followed by server 4.

This data is stored in a proper way in a list.

After all 4 files have been recieved, the file is opened and written in sequence.

--------------------------------------------------------------
3. List

After authenticating, list function send request to each server to send the files and their parts.

Uniques names are added to a list while all the filenames with their extention number are added to another list.

This extentin number list is then compared to uniques names and checked for all 4 parts of the file.

if all the 4 parts are found, the client adds this file to complete list else itll add it to incomplete list.

These lists are then printed.
=====================================================================