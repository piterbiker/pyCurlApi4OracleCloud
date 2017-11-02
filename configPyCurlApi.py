import os

from methodsPickle import PikleToken

DEBUG = True
tokenObject = PikleToken(kat = os.getcwd(), plik = 'pikle')

# cloud account config
identityDomainId = ''
user = ''
password = ''
userEndpoint = ''

CURL_DIR = r''

# compound data
appContHeader = 'X-ID-TENANT-NAME:{}'.format(identityDomainId)
curlPath = os.path.join(CURL_DIR, 'curl.exe')
creditString = '{}:{}'.format(user, password)
storageSrv = 'Storage-{}'.format(identityDomainId)
storageUser = 'X-Storage-User: {}:{}'.format(storageSrv, user)
storagePass = 'X-Storage-Pass: {}'.format(password)

authToken = tokenObject.pickleOdczyt()
XauthToken = 'X-Auth-Token: {}'.format(authToken)

# -------------------------------------------------------------------------------------------
# user's database, services, containers
db = [

    ]
services = [

    ]

containers = [

    ]

# -------------------------------------------------------------------------------------------
# account links: Application Container
userServices = '{}/service/apaas/api/v1.1/apps/{}'.format(userEndpoint, identityDomainId)
userStorage = 'https://{}.storage.oraclecloud.com'.format(identityDomainId)
userStorageAuth = '{}/auth/v1.0'.format(userStorage)
userStorageService = '{}/v1/{}'.format(userStorage, storageSrv)
userStorageCont = '{}/{}'.format(userStorageService, containers[0])


# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print (
        appContHeader, 
        curlPath, 
        creditString, 
        userServices, 
        userStorage, 
        userStorageAuth, 
        userStorageService, 
        userStorageCont, 
        authToken, 
        sep = '\n'
    )



