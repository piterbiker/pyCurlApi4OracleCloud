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
    user, db, services, container, curlPath, DEBUG
    )


class CommonContainer(object):
    '''
    Common class for Application Container & Storage Classic objects 
    '''
    def getDefault(self, curlStr, curlArray):
        curlStrFinal = (curlStr.format(*curlArray)).replace(curlPath, 'curl')
        if DEBUG:
            print (curlStrFinal)
        with open('output.sh', 'w') as textFile:
            textFile.write(curlStrFinal)

        p = subprocess.Popen(
            curlArray,
            stdout=sys.stdout
            )


class AppContainer(CommonContainer):
    '''
    REST API Methods for managing applications in Application container 
    '''
    def __init__(self):
        # templates for cURL commands
        self.curlStr = r"""{} {} {} {} {} {} \
  {} {} \
  {}"""

        self.curlStrCreate = self.curlStr + r""" {} \
  {} {} {} {} {} {} \
  {} {} {} {} \
  {} {} \
  {} {} {} {} \
  {}"""

        self.curlStrUpdate = self.curlStr + r""" {} \
  {} {} {} {} \
  {} {} {} {} \
  {}"""

        # attributes array for Application Container's cURL commands
        self.appContArray = [
        curlPath,
        '-i',
        '-X',
        'GET',
        '--user',
        creditString, 
        '-H',
        '"{}"'.format(appContHeader), 
        userServices
    ]


    def getViewAllApplications(self):
        '''
        Retrieves all applications in the identity domain.
        '''
        self.getDefault(self.curlStr, self.appContArray)


    def getViewApplicationDetails(self, appName):
        '''
        Returns detailed information about an application.
        '''
        self.appContArray[8] = '{}/{}'.format(userServices, appName)
        self.getDefault(self.curlStr, self.appContArray)


    def getViewAllApplicationsDetails(self):
        '''
        Returns detailed information about an application: for all application.
        '''
        for service in services:
            self.getViewApplicationDetails(service)


    def postStartApplication(self, appName):
        '''
        Starts an application
        '''
        self.appContArray[3] = 'POST'
        self.appContArray[8] = '{}/{}/start'.format(userServices, appName)
        self.getDefault(self.curlStr, self.appContArray)


    def postStopApplication(self, appName):
        '''
        Stop an application
        '''
        self.appContArray[3] = 'POST'
        self.appContArray[8] = '{}/{}/stop'.format(userServices, appName)
        self.getDefault(self.curlStr, self.appContArray)


    def postCreateApplication(self, appName, runtime, archiveURL, notes):
        '''
        Create an Application
        '''
        self.appContArray[3] = 'POST'
        self.appContArray[8] = '-H'

        appContArrayCreate = [
            '"Content-Type: multipart/form-data"', 
            '-F', 
            '"name={}"'.format(appName), 
            '-F', 
            '"runtime={}"'.format(runtime), 
            '-F', 
            '"subscription=Monthly"', 
            '-F', 
            '"manifest=@manifest.json"',    # '"manifest={}/manifest.json"'.format(container), 
            '-F', 
            '"deployment=@deployment.json"', 
            '-F', 
            '"archiveURL={}"'.format(archiveURL), 
            '-F',             
            '"notificationEmail={}"'.format(user), 
            '-F', 
            '"notes={}"'.format(notes), 
            userServices
        ]

        self.appContArray += appContArrayCreate
        self.getDefault(self.curlStrCreate, self.appContArray)


    def postDeleteApplication(self, appName):
        '''
        Deletes an application. Returns details about the application being deleted.
        '''
        self.appContArray[3] = 'DELETE'
        self.appContArray[8] = '{}/{}'.format(userServices, appName)
        self.getDefault(self.curlStr, self.appContArray)


    def putUpdatesApplication(self, appName, archiveURL, notes):
        '''
        Updates an Oracle Application Container Cloud Service Application
        '''
        self.appContArray[3] = 'PUT'
        self.appContArray[8] = '-H'
    
        appContArrayUpdate = [
            '"Content-Type: multipart/form-data"', 
            '-F', 
            '"manifest=@manifest.json"', 
            '-F', 
            '"deployment=@deployment.json"', 
            '-F', 
            '"archiveURL={}"'.format(archiveURL), 
            '-F', 
            '"notes={}"'.format(notes), 
            '{}/{}'.format(userServices, appName)
        ]

        self.appContArray += appContArrayUpdate
        self.getDefault(self.curlStrUpdate, self.appContArray)

# -------------------------------------------------------------------------------------------

class StorageClassic(CommonContainer):
    '''
    REST API Methods for managing obects in Storage Classic 
    '''
    def __init__(self):
        # templates for cURL commands
        self.curlStrInfo = r"""{} {} {} {} \
  {} {} \
  {}"""

        self.curlStr = self.curlStrInfo + r""" {} \
  {}"""

        #attributes array for Storage's Classic cURL commands
        self.storageClInfoArray = [
            curlPath,
            '-v',
            '-X',
            'GET',
            '-H',
            XauthToken,
            userStorageService
        ]

    
    def getRequestAuthenticationToken(self):
        '''
        Requesting an authentication token.
        '''
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

        self.getDefault(self.curlStr, storageClAuthArray)


    def getShowAccountDetails(self):
        '''
        Show account details and list containers.
        '''
        self.getDefault(self.curlStrInfo, self.storageClInfoArray)


    def getShowContainerDetails(self):
        '''
        Show container details and list objects.
        '''
        self.storageClInfoArray[6] = userStorageCont
        self.getDefault(self.curlStrInfo, self.storageClInfoArray)


    def getGetObjectContent(self, remoteFile):
        '''
        Get object content and metadata.
        '''
        self.storageClInfoArray[6] = '-o'
        self.storageClInfoArray.append(os.path.join('data', remoteFile.replace('/', '_')))
        self.storageClInfoArray.append('{}/{}'.format(userStorageCont, remoteFile))
        self.getDefault(self.curlStr, self.storageClInfoArray)


    def putCreateReplaceObject(self, localFile, remoteFile):
        '''
        Create or replace object.
        '''
        self.storageClInfoArray[3] = 'PUT'
        self.storageClInfoArray[6] = '-T'
        self.storageClInfoArray.append(os.path.join('data', localFile))
        self.storageClInfoArray.append('{}/{}'.format(userStorageCont, remoteFile))
        self.getDefault(self.curlStr, self.storageClInfoArray)

