import os
import sys
import json
import pprint
import subprocess

import requests

from configPyCurlApi import (
    # Application Container
    appContHeader, creditString, userServices, 
    # Storage Classic
    storageUser, storagePass, 
    XauthToken, userStorageAuth, userStorageService, userStorageCont, 
    # other
    db, services, curlPath, DEBUG
    )

# attributes array for Application Container
appContArray = [
    curlPath,
    '-i',
    '-X',
    'GET',
    '-u',
    creditString,
    '-H',
    '"{}"'.format(appContHeader), 
    userServices
]

# attributes array for Storage Classic
storageClAuthArray = [
    curlPath,
    '-v',
    '-X',
    'GET',
    '-H',
    storageUser,
    '-H',
    storagePass, 
    userStorageAuth
]

storageClInfoArray = [
    curlPath,
    '-v',
    '-X',
    'GET',
    '-H',
    XauthToken,
    userStorageService
]


# -------------------------------------------------------------------------------------------
# REST API for Managing Applications methods
def getDefault(endString=None):
    curlStr = r"""
{} {} {} {} {} {} \
  {} {} \
  {}""".format(*appContArray)

    if DEBUG:
        print (curlStr)
    with open('output.sh', "w") as textFile:
        textFile.write(curlStr + '\n')

    p = subprocess.Popen(
        appContArray,
        stdout=sys.stdout
        )

def getViewAllApplications():
    '''
    Retrieves all applications in the identity domain.
    '''
    getDefault()


def getViewApplicationDetails(appName):
    '''
    Returns detailed information about an application.
    '''
    appContArray[8] = '{}/{}'.format(userServices, appName)
    getDefault()


def getViewAllApplicationsDetails():
    '''
    Returns detailed information about an application: for all application.
    '''
    for service in services:
        getViewApplicationDetails(service)


def postStartApplication(appName):
    '''
    Starts an application
    '''
    appContArray[3] = 'POST'
    appContArray[8] = '{}/{}/start'.format(userServices, appName)
    getDefault()


def postStopApplication(appName):
    '''
    Stop an application
    '''
    appContArray[3] = 'POST'
    appContArray[8] = '{}/{}/stop'.format(userServices, appName)
    getDefault()


def postCreateApplication(appName, notes, archiveURL, runtime):
    '''
    Create an Application
    '''
    global appContArray
    appContArray[3] = 'POST'
    appContArray[8] = '-H'

    appContArrayCreate = [
        '"Content-Type: multipart/form-data"', 
        '-F', 
        '"name={}"'.format(appName), 
        '-F', 
        '"runtime={}"'.format(runtime), 
        '-F', 
        '"subscription=Monthly"', 
        '-F', 
        '"manifest=@manifest.json"', 
        '-F', 
        '"deployment=@deployment.json"', 
        '-F', 
        '"archiveURL={}"'.format(archiveURL), 
        '-F', 
        '"notes={}"'.format(notes), 
        userServices
    ]

    appContArray += appContArrayCreate
    print(*appContArray, sep = '\n')
    getDefault()




# -------------------------------------------------------------------------------------------
# REST API for Standard Storage in Oracle Cloud 
# Infrastructure Object Storage Classic
def getDefaultStorage(arrayCloud):
    p = subprocess.Popen(
        arrayCloud,
        stdout=sys.stdout
        )

    
def getRequestAuthenticationToken():
    '''
    Requesting an authentication token.
    '''
    getDefaultStorage(storageClAuthArray)


def getShowAccountDetails():
    '''
    Show account details and list containers.
    '''
    getDefaultStorage(storageClInfoArray)


def getShowAccountDetails():
    '''
    Show account details and list containers.
    '''
    getDefaultStorage(storageClInfoArray)


def getShowContainerDetails():
    '''
    Show container details and list objects,
    '''
    storageClInfoArray[6] = userStorageCont
    getDefaultStorage(storageClInfoArray)


def getGetObjectContent(localFile, remoteFile):
    '''
    Get object content and metadata.
    '''
    storageClInfoArray[6] = '-o'
    storageClInfoArray.append(os.path.join('data', localFile))
    storageClInfoArray.append('{}/{}'.format(userStorageCont, remoteFile))
    getDefaultStorage(storageClInfoArray)


def putCreateReplaceObject(localFile, remoteFile):
    '''
    Create or replace object.
    '''
    storageClInfoArray[3] = 'PUT'
    storageClInfoArray[6] = '-T'
    storageClInfoArray.append(os.path.join('data', localFile))
    storageClInfoArray.append('{}/{}'.format(userStorageCont, remoteFile))
    getDefaultStorage(storageClInfoArray)

# -------------------------------------------------------------------------------------------
# TODO: Python requests as cURL

#headers = {
#    appContHeader
#}

#r = requests.get(
#    adres,
#    headers=headers,
#    auth=(user, haslo)
#    )

#nagl = r.headers
#data = r.json()

#pprint.pprint(dict(nagl), width=1)
#print (80*'-'+'\n')
#pprint.pprint(data, width=1)
#print ('\n')





