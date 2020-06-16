import json
import pandas as pd

csvSourcePath00 = './sampleCSV/2017_12.csv'
csvSourcePath01 = './sampleCSV/2014_10.csv'
csvSourcePath02 = './sampleCSV/2018_05.csv'


csvPathArr = [csvSourcePath00, csvSourcePath01,
              csvSourcePath02]

for i in range(len(csvPathArr)):
    df = pd.read_csv(csvPathArr[i], names=['Time', 'Frequency'])
    timeArr = df['Time']
    freqArr = df['Frequency']

    freqJson = open(f'./output/frequency_{i}.json', 'w+')
    timeJson = open(f'./output/time_{i}.json', 'w+')

    json.dump(freqArr.tolist(), freqJson)
    json.dump(timeArr.tolist(), timeJson)
    freqJson.close()
    timeJson.close()
