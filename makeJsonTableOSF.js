const fs = require("fs");
const path = require("path");

const OUTPUT_DIR = 'output'
const OUTPUT_JSON = 'tableJsonOsf.json'
const repoStructureJsonPath = path.resolve(__dirname, "output", "output_pathsAndLinks.json");

async function getRepoStructure(repoStructureJsonPath) {
  const tableJson = [];

  const jsonTxt = fs.readFileSync(repoStructureJsonPath, { encoding: "utf8" });
  repoStructure = JSON.parse(jsonTxt);

  let found = 0;
  repoStructure.forEach((branch, index) => {
    // if (branch.path.includes(".zip")) {
    found += 1;
    const currentDownloadURL = branch.url

    pushToTableJson(branch.path, tableJson, currentDownloadURL, found);
    // }
  });

  return new Promise((resolve, reject) => {
    resolve(tableJson);
  });
}

function pushToTableJson(apiPath, tableJson, downloadURL, found) {
  const arrayfiedApiPath = apiPath.split(`/`);

  indexOffset = 2 // since ['', 'Data', 'Realm', 'Country', ...etc] for OSF.
  const realm = arrayfiedApiPath[0 + indexOffset];
  const country = arrayfiedApiPath[1 + indexOffset];
  const year = arrayfiedApiPath[2 + indexOffset];
  const month = arrayfiedApiPath[3 + indexOffset];
  const fileName = arrayfiedApiPath[4 + indexOffset];

  if (found === 1) {
    tableJson.push(getNewRealm(realm, country, year, month, downloadURL));
  } else {
    if (currentRealm !== realm) {
      tableJson.push(getNewRealm(realm, country, year, month, downloadURL));
    } else if (currentRealm === realm && currentCountry !== country) {
      tableJson.forEach((_realm) => {
        if (_realm["name"] === currentRealm) {
          _realm.children.push(getNewCountry(country, year, month, downloadURL));
        }
      });
    } else if (currentRealm === realm && currentCountry === country && currentYear !== year) {
      tableJson.forEach((_realm) => {
        if (_realm["name"] === currentRealm) {
          _realm.children.forEach((_country) => {
            if (_country["name"] === currentCountry) {
              _country.children.push(getNewYear(year, month, downloadURL));
            }
          });
        }
      });
    } else if (currentRealm === realm && currentCountry === country && currentYear === year && currentMonth !== month) {
      tableJson.forEach((_realm) => {
        if (_realm["name"] === currentRealm) {
          _realm.children.forEach((_country) => {
            if (_country["name"] === currentCountry) {
              // _country.children.push(getNewYear(year, month, downloadURL));
              _country.children.forEach((_year) => {
                if (_year["name"] === currentYear) {
                  _year.children.push(getNewMonth(month, downloadURL));
                }
              });
            }
          });
        }
      });
    }
  }

  currentRealm = realm;
  currentCountry = country;
  currentYear = year;
  currentMonth = month;
  currentFileName = fileName;
}

function getNewRealm(realm, country, year, month, downloadURL) {
  return {
    name: realm,
    type: "folder",
    tabSystem: true,
    children: [getNewCountry(country, year, month, downloadURL)],
  };
}

function getNewCountry(country, year, month, downloadURL) {
  return {
    name: country,
    type: "folder",
    tabSystem: true,
    children: [getNewYear(year, month, downloadURL)],
  };
}

function getNewYear(year, month, downloadURL) {
  return {
    name: year,
    type: "folder",
    children: [getNewMonth(month, downloadURL)],
  };
}

function getNewMonth(month, downloadURL) {
  return {
    name: month,
    type: "folder",
    children: [
      {
        name: "Data",
        type: "file",
        downloadURL: downloadURL,
      },
    ],
  };
}


getRepoStructure(repoStructureJsonPath).then((outputTableJson) => {
  // write json output
  fs.writeFileSync(
    path.resolve(__dirname, OUTPUT_DIR, OUTPUT_JSON),
    JSON.stringify(outputTableJson, null, 2)
  );
});

