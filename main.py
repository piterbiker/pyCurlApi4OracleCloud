from methodsPyCurlApi import (
    # Application Container
    AppContainer, 

    # Storage Classic
    StorageClassic
    )


def main():
    '''
    Enter necessary methods here
    '''
    appContainerObject = AppContainer()
    appContainerObject.getViewAllApplications()
    input()


if __name__ == '__main__':
    main()
