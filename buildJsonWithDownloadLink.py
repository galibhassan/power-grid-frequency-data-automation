import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome()

mainSiteURL = 'https://github.com/LRydin/Power-Grid-Frequency-data'

# loading the page
driver.get(mainSiteURL)

folderIcons_all = driver.find_elements_by_class_name(
    'octicon octicon-file-directory')

print('wait')
