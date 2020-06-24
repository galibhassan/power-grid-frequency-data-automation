const fs = require("fs");
const path = require("path");
const fetch = require("node-fetch");

async function getRepoStructure(repoStructureJsonPath) {
  const tableJson = [];

  const jsonTxt = fs.readFileSync(repoStructureJsonPath, { encoding: "utf8" });
  repoStructure = JSON.parse(jsonTxt);

  let currentRealm = "";
  let currentCountry = "";
  let currentYear = "";
  let currentMonth = "";
  let currentFileName = "";

  let found = 0;
  repoStructure.tree.forEach((branch, index) => {
    if (branch.path.includes(".zip")) {
      found += 1;
      const currentDownloadURL = getGithubURLFromAPIPath(branch.path);
      pushToTableJson(branch.path, tableJson, currentDownloadURL, found);
    }
  });

  return new Promise((resolve, reject) => {
    resolve(tableJson);
  });
}

function pushToTableJson(apiPath, tableJson, downloadURL, found) {
  const arrayfiedApiPath = apiPath.split(`/`);

  const realm = arrayfiedApiPath[0];
  const country = arrayfiedApiPath[1];
  const year = arrayfiedApiPath[2];
  const month = arrayfiedApiPath[3];
  const fileName = arrayfiedApiPath[4];

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
    children: [
      {
        name: country,
        type: "folder",
        children: [
          {
            name: year,
            type: "folder",
            children: [
              {
                name: month,
                type: "folder",
                children: [
                  {
                    name: "Data",
                    type: "file",
                    downloadURL: downloadURL,
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  };
}

function getNewCountry(country, year, month, downloadURL) {
  return {
    name: country,
    type: "folder",
    children: [
      {
        name: year,
        type: "folder",
        children: [
          {
            name: month,
            type: "folder",
            children: [
              {
                name: "Data",
                type: "file",
                downloadURL: downloadURL,
              },
            ],
          },
        ],
      },
    ],
  };
}

function getNewYear(year, month, downloadURL) {
  return {
    name: year,
    type: "folder",
    children: [
      {
        name: month,
        type: "folder",
        children: [
          {
            name: "Data",
            type: "file",
            downloadURL: downloadURL,
          },
        ],
      },
    ],
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

/**
 * @returns {String} download-url for zip file
 *
 * */
function getGithubURLFromAPIPath(apiPath) {
  const apiPath_noSpace = apiPath.replace(" ", "%20");
  const fileUrlHead = "https://github.com/LRydin/Power-Grid-Frequency-Data/raw/master/";
  return fileUrlHead + apiPath_noSpace;
}

const repoStructureJsonPath = path.resolve(__dirname, "output", "output.json");
getRepoStructure(repoStructureJsonPath).then((outputTableJson) => {
  // write json output
  fs.writeFileSync(
    path.resolve(__dirname, "output", "powerGridDataTableInfo.json"),
    JSON.stringify(outputTableJson, null, 2)
  );
});
