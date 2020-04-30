#!/usr/bin/env python
import sys
import glob
import json
import os.path
import xml.etree.ElementTree as ET

def writeJsonToFile(json_dump, globPattern, fileType):
    if 'master' in globPattern[0]:
        fileName = 'master-coverage-report.json'
    else:
        fileName = 'pr-coverage-report.json'

    # check if coverage file already exists and read data from it and add in current dump 
    old_json = {}
    if os.path.isfile(fileName):
        with open(fileName, 'r') as json_old_file:
            old_json = json.load(json_old_file)
    
    with open(fileName, 'w') as json_file:
        if old_json:
            for key in old_json.keys():
                json_dump[key] = old_json.get(key)

        json.dump(json_dump, json_file)

def parseCobertura(files):
    # required attributes from cobertura coverage
    coverage_metrics = {
        'lines-valid': 0,
        'line-rate': 0,
        'lines-covered': 0,
    }
     
    for file in files:
        try:
            root = ET.parse(file).getroot()
            for attribute in root.attrib:
                if attribute in coverage_metrics.keys():
                    coverage_metrics[attribute] = float(root.get(attribute))
        except Exception as e:
            print "Unable to parse {}. {}".format(file, e)

    return coverage_metrics

def parseJest(files):
    # required attributes from jest coverage
    coverage_metrics = {
        'tests': 0,
        'failures': 0,
        'skipped': 0,
    }
    
    for file in files:
        try:
            root = ET.parse(file).getroot()
            testsuites = root.findall('./testsuite')
            
            for testsuite in testsuites:
                for attribute in testsuite.attrib:
                    if attribute in coverage_metrics.keys():
                        coverage_metrics[attribute] += float(testsuite.get(attribute))
                        
        except Exception as e:
            print "Unable to parse {}. {}".format(file, e)
    return coverage_metrics

# parse xml to json based on file type
def getJsonFromXml(fileName, fileType):
    
    coverage_metrics = parseCobertura(fileName) if fileType == "cobertura" else parseJest(fileName)
    return coverage_metrics


def main(globPattern, fileType):
    
    json_dump = getJsonFromXml(globPattern, fileType)
    writeJsonToFile(json_dump, globPattern, fileType)

if __name__ == '__main__':
    # get file name with complete path
    globPattern = glob.glob(sys.argv[1])

    if not globPattern:
        sys.exit("xmlToJson.py: input file not found, make sure file already exists")

    if not globPattern[0].endswith('.xml'):
        sys.exit("xmlToJson.py: invalid file extension, allowed extensions: .xml")

    # get fileType to be parsed. allowed fileTypes: cobertura and jest
    # TODO: check for argument key as well
    fileType = sys.argv[2].split('=')[1]
    if fileType.lower() not in ['cobertura', 'jest']:
        sys.exit("xmlToJson.py: received invalid file type argument, allowed filetypes: cobertura/jest-junit")
    
    sys.exit(main(globPattern, fileType))