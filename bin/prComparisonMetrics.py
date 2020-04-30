#!/usr/bin/env python
import sys
import glob
import json
import os.path
from texttable import Texttable

def validateFiles(files):

    for file in files:
        if os.path.isfile(file) and file.endswith('.json'):
            isValid = True
        else:
            isValid = False
            print "invalid input file: {}, make sure the file exists and ends with .json".format(file)
    return isValid

def generateDelta(baseline, pr):
    delta = {}
    # validate both baseline and pr contains same keys
    for key in baseline.keys():
        if key not in pr.keys():
            raise ValueError('Unable to generate Delta, both files must have same keys')
        else:
            delta[key] = abs(baseline.get(key) - pr.get(key))
    
    return delta



def generateComparisionMetrics(files):
    pr_metrics = {}
    baseline_metrics = {}
    delta = {}
    comparision_metrics = {}

    for file in files:
        if 'master' in file:
            with open(file, 'r') as json_file:
                baseline_metrics = json.load(json_file)
                comparision_metrics['baseline'] = baseline_metrics
        else:
            with open(file, 'r') as json_file:
                pr_metrics = json.load(json_file)
                comparision_metrics['PR'] = pr_metrics
    
    delta = generateDelta(baseline_metrics, pr_metrics)
    comparision_metrics['delta'] = delta
    return comparision_metrics

def buildTabularData(jsonResult):
    tableMapping = {
        'Skipped Test': 'skipped',
        'Failed Test': 'failures',
        'Total Test': 'tests',
        'Line Coverage': 'line-rate',
        'Uncovered Lines': 'uncovered lines',
        'Total Lines': 'lines-valid'
    }
    
    table = """|{:-^20}|{:-^20}|{:-^20}|{:-^20}|""".format('Metrics', 'Baseline', 'PR', 'Delta')
    for key in tableMapping.keys():
        attribute = tableMapping.get(key)
        pr = jsonResult.get('PR').get(attribute)
        baseline = jsonResult.get('baseline').get(attribute)
        delta = jsonResult.get('delta').get(attribute)

        # line coverage to be displayed as percentage
        if key is 'Line Coverage':
            pr *= 100
            baseline *= 100
            delta *= 100
        
        if key is 'Uncovered Lines':
            pr = jsonResult.get('PR').get('lines-valid') - jsonResult.get('PR').get('lines-covered')
            baseline = jsonResult.get('baseline').get('lines-valid') - jsonResult.get('baseline').get('lines-covered')
            delta = jsonResult.get('delta').get('lines-valid') - jsonResult.get('delta').get('lines-covered')
        
        # table.add_row([key, baseline, pr, delta])
        row = """\n|{: <20}|{: <20}|{: <20}|{: <20}|""".format(key,baseline,pr,delta)
        table = table + row
    
    # print table.draw()
    # print type(table)
    # print type(table.draw.__str__())
    # return table._fmt_text(table)
    # baseline = jsonResult.get('baseline')
    # pr = jsonResult.get('PR')
    # delta = jsonResult.get('delta')
    # table = """
    #     |----Metrics-----|----BaseLine----|----PR-----|----Delta----|
    #     |Skipped Test    |{:20}|{:20}|{:20}|
    #     |Failed Test     |{:20}|{:20}|{:20}|
    #     |Total Test      |{:20}|{:20}|{:20}|
    #     |Line Coverage   |{:20}|{:20}|{:20}|
    #     |uncovered lines |{:20}|{:20}|{:20}|
    #     |Total Lines     |{:20}|{:20}|{:20}|
    #     |----------------|----------------|-----------|-------------|
    # """.format(baseline.get('skipped'), pr.get('skipped'), delta.get('skipped'),
    #     baseline.get('failures'), pr.get('failures'), delta.get('failures'),
    #     baseline.get('tests'), pr.get('tests'), delta.get('tests'),
    #     baseline.get('line-rate')*100, pr.get('line-rate')*100, delta.get('line-rate')*100,
    #     baseline.get('lines-valid') - baseline.get('lines-covered'), pr.get('lines-valid') - pr.get('lines-covered'), delta.get('lines-valid') - delta.get('lines-covered'),
    #     baseline.get('lines-valid'), pr.get('lines-valid'), delta.get('lines-valid'),
    # )

    # return table.draw()
    return table





def main(files):
    result = generateComparisionMetrics(files)
    if result:
        return buildTabularData(result)
    else:
        return "Unable to generate metrics"

if __name__ == '__main__':
    inputFiles = [sys.argv[1], sys.argv[2]]
    isValidArgs = validateFiles(inputFiles)

    if isValidArgs:
        result = main(inputFiles)
        sys.stdout.write(result)
        sys.stdout.flush()
        sys.exit()
    else:
        sys.exit()