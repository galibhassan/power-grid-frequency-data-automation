''' 
  This program creates a json file with download-links by using OSF api.
  It will only collect the info of the data inside the folder with handle: DATA_WRAPPER_FOLDER_HANDLE.
  Please change the values of the capitalized variables according to your need. 
'''

import requests
import json

SEARCHED_FILE_EXTENSION = ".csv"
OSF_NODE_HANDLE = 'by5hu'
DATA_WRAPPER_FOLDER_HANDLE = "5ec248d3b9daae00b4508576"
OUTPUT_JSON_PATH = './output/OneSecondRes.json'

baseurl_osf = f'https://api.osf.io/v2/nodes/{OSF_NODE_HANDLE}/files/osfstorage/{DATA_WRAPPER_FOLDER_HANDLE}/'
downloadInfoStorage = []


def getDictFromRequest(baseurl):
    response = requests.get(baseurl)
    dict_json = json.loads(response.text)
    return dict_json


def getRepoStructure(baseurl):
    currentStructure = getDictFromRequest(baseurl)

    currentSubStructures = currentStructure["data"]
    for i in range(len(currentSubStructures)):

        if currentSubStructures[i]['attributes']['kind'] == "folder":
            # recurse, i.e. make another get request on baseurl+element.id
            newURL = currentSubStructures[i]['relationships']['files']['links']['related']['href']
            getRepoStructure(newURL)

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


def writeIntoJson(structureDict, jsonPath):
    jsonFile = open(jsonPath, 'w+')
    json.dump(structureDict, jsonFile, indent=2)
    jsonFile.close()


def main():
    getRepoStructure(baseurl_osf)
    writeIntoJson(downloadInfoStorage, OUTPUT_JSON_PATH)


main()
