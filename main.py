from methodsPyCurlApi import (
    # Application Container
    # GET
    getViewAllApplications, getViewApplicationDetails, getViewAllApplicationsDetails, 
    # POST
    postStartApplication, postStopApplication, postCreateApplication, 

    # Storage Classic
    # GET
    getRequestAuthenticationToken, 
    getShowAccountDetails, getShowContainerDetails, 
    getGetObjectContent, putCreateReplaceObject
    )

def main():
    '''
    enter necessary methods here
    '''
    
    getViewAllApplications()

    input()


if __name__ == '__main__':
    main()
