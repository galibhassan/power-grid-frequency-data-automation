import json

OUTPUT_JSON_PATH = './output/mewwwtableJsonOsf.json'
repoStructureJsonPath = "./output/output_pathsAndLinks.json"


def getRepoStructure(repoStructureJsonPath):
    tableJson = []
    repoStructureFile = open(repoStructureJsonPath)
    repoStructure = json.load(repoStructureFile)

    found = 0
    for i in range(len(repoStructure)):
        branch = repoStructure[i]
        found += 1
        currentDownloadURL = branch['url']
        pushToTableJson(branch['path'], tableJson, currentDownloadURL, found)

    return tableJson


# declaration
currentRealm = ''
currentCountry = ''
currentYear = ''
currentMonth = ''
currentFileName = ''


def pushToTableJson(apiPath, tableJson, downloadURL, found):
    global currentRealm
    global currentCountry
    global currentYear
    global currentMonth
    global currentFileName

    arrayfiedApiPath = apiPath.split('/')

    indexOffset = 2  # since for OSF ['', 'Data', 'Realm', 'Country', ...etc]
    realm = arrayfiedApiPath[0 + indexOffset]
    country = arrayfiedApiPath[1 + indexOffset]
    year = arrayfiedApiPath[2 + indexOffset]
    month = arrayfiedApiPath[3 + indexOffset]
    fileName = arrayfiedApiPath[4 + indexOffset]

    if found == 1:
        tableJson.append(getNewRealm(realm, country, year, month, downloadURL))
    else:
        if currentRealm != realm:
            tableJson.append(getNewRealm(
                realm, country, year, month, downloadURL))
        elif currentRealm == realm and currentCountry != country:
            for i in range(len(tableJson)):
                _realm = tableJson[i]
                if _realm["name"] == currentRealm:
                    _realm['children'].append(getNewCountry(
                        country, year, month, downloadURL))

        elif currentRealm == realm and currentCountry == country and currentYear != year:
            for i in range(len(tableJson)):
                _realm = tableJson[i]
                if _realm["name"] == currentRealm:
                    for j in range(len(_realm['children'])):
                        _country = _realm['children'][j]
                        if _country["name"] == currentCountry:
                            _country['children'].append(
                                getNewYear(year, month, downloadURL))

        elif currentRealm == realm and currentCountry == country and currentYear == year and currentMonth != month:
            for i in range(len(tableJson)):
                _realm = tableJson[i]
                if _realm["name"] == currentRealm:
                    for j in range(len(_realm['children'])):
                        _country = _realm['children'][j]
                        if _country["name"] == currentCountry:
                            for k in range(len(_country['children'])):
                                _year = _country['children'][k]
                                if _year["name"] == currentYear:
                                    _year["children"].append(
                                        getNewMonth(month, downloadURL))

    currentRealm = realm
    currentCountry = country
    currentYear = year
    currentMonth = month
    currentFileName = fileName

# ---------------


def getNewRealm(realm, country, year, month, downloadURL):
    return {
        "name": realm,
        "type": "folder",
        "tabSystem": True,
        "children": [getNewCountry(country, year, month, downloadURL)],
    }


def getNewCountry(country, year, month, downloadURL):
    return {
        "name": country,
        "type": "folder",
        "tabSystem": True,
        "children": [getNewYear(year, month, downloadURL)],
    }


def getNewYear(year, month, downloadURL):
    return {
        "name": year,
        "type": "folder",
        "children": [getNewMonth(month, downloadURL)],
    }


def getNewMonth(month, downloadURL):
    return {
        "name": month,
        "type": "folder",
        "children": [
            {
                "name": "Data",
                "type": "file",
                "downloadURL": downloadURL,
            },
        ],
    }


tableJsonOSF = getRepoStructure(repoStructureJsonPath)
outputJson = open(OUTPUT_JSON_PATH, 'w+')
json.dump(tableJsonOSF, outputJson, indent=2)
outputJson.close()