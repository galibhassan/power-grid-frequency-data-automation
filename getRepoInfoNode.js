const fs = require("fs");
const path = require("path");
const fetch = require("node-fetch");

const repoOwner = "LRydin";
const repoName = "Power-Grid-Frequency-Data";
const branchName = "master";
const baseurl = `https://api.github.com/repos/${repoOwner}/${repoName}/git/trees/${branchName}?recursive=1`;

async function getRepoStructure(baseurl) {
  const repoStructure_response = await fetch(baseurl);
  const repoStructure = await repoStructure_response.json();
  // write json output
  fs.writeFileSync(
    // path.resolve(path.join(__dirname, "output", repoName, "_", repoName, "_", branchName)),
    path.resolve(__dirname, "output", "output.json"),
    JSON.stringify(repoStructure, null, 2)
  );
}

getRepoStructure(baseurl);
