'''
  This program creates a json file with download-links by using OSF api.
  It will only collect the info of the data inside the folder with handle: DATA_WRAPPER_FOLDER_HANDLE.
  Please change the values of the capitalized variables according to your need.
'''

import requests
import json
import eel

eel.init('./web')


def getDictFromRequest(baseurl):
    response = requests.get(baseurl)
    dict_json = json.loads(response.text)
    return dict_json


def getRepoStructure(baseurl, osfCredentials, downloadInfoStorage):

    SEARCHED_FILE_EXTENSION = osfCredentials['SEARCHED_FILE_EXTENSION']

    currentStructure = getDictFromRequest(baseurl)

    currentSubStructures = currentStructure["data"]
    for i in range(len(currentSubStructures)):

        if currentSubStructures[i]['attributes']['kind'] == "folder":
            # recurse, i.e. make another get request on baseurl+element.id
            newURL = currentSubStructures[i]['relationships']['files']['links']['related']['href']
            getRepoStructure(newURL, osfCredentials, downloadInfoStorage)

        else:
            """
              i.e.  if  (element.attributes.kind === "file")
              check if it satisfies file-extension. if true, then collect:
              - attribute.materialized_path
              - download link
            """

            fileName = currentSubStructures[i]['attributes']['name']

            if SEARCHED_FILE_EXTENSION in fileName:
                path = currentSubStructures[i]['attributes']['materialized_path']
                downloadURL = currentSubStructures[i]['links']['download']
                downloadInfoStorage.append({
                    "path": path,
                    "url": downloadURL
                })


def writeIntoJson(structureDict, osfCredentials):
    jsonPath = osfCredentials['OUTPUT_JSON_PATH']
    jsonFile = open(jsonPath, 'w+')
    json.dump(structureDict, jsonFile, indent=2)
    jsonFile.close()


@eel.expose
def main_getRepoInfoOSFGUI(osfCredentials):

    # OUTPUT_JSON_PATH = osfCredentials['OUTPUT_JSON_PATH']
    OSF_NODE_HANDLE = osfCredentials['OSF_NODE_HANDLE']
    DATA_WRAPPER_FOLDER_HANDLE = osfCredentials['DATA_WRAPPER_FOLDER_HANDLE']
    baseurl_osf = f'https://api.osf.io/v2/nodes/{OSF_NODE_HANDLE}/files/osfstorage/{DATA_WRAPPER_FOLDER_HANDLE}/'

    try:
        downloadInfoStorage = []
        getRepoStructure(baseurl_osf, osfCredentials, downloadInfoStorage)
        writeIntoJson(downloadInfoStorage, osfCredentials)
        return 'success'
    except:
        return 'error'


@eel.expose
def dummyFunc(osfCredentials):
    print('osfCredentials from client side')
    print(osfCredentials)


eel.start('index.html', size=(620, 445))
# eel.start('index.html')
