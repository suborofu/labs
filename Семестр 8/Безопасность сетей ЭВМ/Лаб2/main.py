from FTP import FTP

ftp_server = FTP()

while True:
    IP = input('IP:\t\t\t')
    user = input('Username:\t')
    password = input('Password:\t')
    if ftp_server.connect(IP, user, password):
        print("Connected\n")
        break
    print("IP, username, or password is not valid\n")

help = """
ls              Lists the current folder's content
cd {folder}     Makes the specified folder the current one
load {file}     Loads the specified file from the server
send {file}     Sends the specified file to the server
quit            Closes the program
"""

print("Type 'help' for detailed information on available options\n")

while True:
    command = input('~' + ftp_server.get_dir() + ': ').split()
    try:
        if command[0] == "ls":
            ftp_server.list_dir()
        elif command[0] == "cd":
            ftp_server.change_dir(command[1])
        elif command[0] == "load":
            ftp_server.load_file(command[1])
            print("Done\n")
        elif command[0] == "send":
            ftp_server.send_file(command[1])
            print("Done\n")
        elif command[0] == "quit":
            break
        elif command[0] == "help":
            print(help)
        else:
            print("Unknown command:\t" + command[0])
    except:
        print("Not enough parameters\n")
