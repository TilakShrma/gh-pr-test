#!/usr/bin/python
import sys
import glob
import json
import os.path
import xml.etree.ElementTree as ET

def main():

    metrics = """
        |----Metrics-----|----BaseLine----|----PR-----|----Delta----|
        |Skipped Test    |      %d        |    %d     |      %d     |
        |Failed Test     |   %d           |      %d   |      %d     |
        |Total Test      |   %d           |      %d   |      %d     |
        |Line Coverage in percentage   |   %d           |      %d   |      %d     |
        |uncovered lines |   %d           |      %d   |      %d     |
        |Total Lines     |   %d           |      %d   |      %d     |
        |----------------|----------------|-----------|-------------|
    """ %(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)
    print metrics

if __name__ == '__main__':
    sys.exit(main())