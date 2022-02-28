import win32api, pickle, hashlib


def checkHDD():
    disk1 = '232f7967e2e4dcdfd4425934ecd857308358a514'
    disk2 = hashlib.sha1(pickle.dumps(win32api.GetVolumeInformation('C:\\'))).hexdigest()
    if disk1 == disk2:
        return True
    else:
        return False


if not checkHDD():
    print('Authentication failed!')
    exit(1)

print('Hello, world')
