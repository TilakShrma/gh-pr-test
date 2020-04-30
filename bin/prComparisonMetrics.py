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



def generateComparisonMetrics(files):
    pr_metrics = {}
    baseline_metrics = {}
    delta = {}
    comparison_metrics = {}

    for file in files:
        if 'master' in file:
            with open(file, 'r') as json_file:
                baseline_metrics = json.load(json_file)
                comparison_metrics['baseline'] = baseline_metrics
        else:
            with open(file, 'r') as json_file:
                pr_metrics = json.load(json_file)
                comparison_metrics['PR'] = pr_metrics
    
    delta = generateDelta(baseline_metrics, pr_metrics)
    comparison_metrics['delta'] = delta
    return comparison_metrics

def generateMetricsTable(metrics):
    baseline = metrics.get('baseline')
    pr = metrics.get('PR')
    delta = metrics.get('delta')
    
    table = """
        |{:-^16}|{:-^9}|{:-^6}|{:-^6}|
        |{:<16}|{:<9}|{:<6}|{:<6}|
        |{:<16}|{:<9}|{:<6}|{:<6}|
        |{:<16}|{:<9}|{:<6}|{:<6}|
        |{:<16}|{:<9}|{:<6}|{:<6}|
        |{:<16}|{:<9}|{:<6}|{:<6}|
        |{:<16}|{:<9}|{:<6}|{:<6}|
        
    """.format('Metrics', 'Baseline', 'PR', 'Delta',
        'Skipped Test', baseline.get('skipped'), pr.get('skipped'), delta.get('skipped'),
        'Failed Test', baseline.get('failures'), pr.get('failures'), delta.get('failures'),
        'Total Test', baseline.get('tests'), pr.get('tests'), delta.get('tests'),
        'Line Coverage %', baseline.get('line-rate')*100, pr.get('line-rate')*100, delta.get('line-rate')*100,
        'uncovered lines', baseline.get('lines-valid') - baseline.get('lines-covered'),
        pr.get('lines-valid') - pr.get('lines-covered'),
        delta.get('lines-valid') - delta.get('lines-covered'),
        'Total Lines', baseline.get('lines-valid'), pr.get('lines-valid'), delta.get('lines-valid'),
    )
    
    return metrics_table

def main(files):
    result = generateComparisonMetrics(files)
    if result:
        return generateMetricsTable(result)
    else:
        print "Unable to generate metrics"

if __name__ == '__main__':
    inputFiles = [sys.argv[1], sys.argv[2]]
    isValidArgs = validateFiles(inputFiles)

    if isValidArgs:
        result = main(inputFiles)
        sys.stdout.write(result)
        sys.stdout.flush()
        sys.exit()
    else:
        sys.exit("invalid args")