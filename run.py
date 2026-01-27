#!/usr/bin/env python3
"""
TenderNed API Example Runner

This script allows you to run either the XML or JSON version of the TenderNed API example.

Usage:
    python run.py              # Run JSON API (default)
    python run.py --json       # Run JSON API explicitly
    python run.py --xml        # Run XML API (limited availability)
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run TenderNed API examples')
    parser.add_argument('--xml', action='store_true', help='Use XML API (limited availability)')
    parser.add_argument('--json', action='store_true', help='Use JSON API (default)')
    
    args = parser.parse_args()
    
    if args.xml:
        print("Running XML API example...")
        print("Note: XML API has limited availability for recent publications\n")
        import tenderned_xml_api_example
        tenderned_xml_api_example.main()
    else:
        print("Running JSON API example...")
        print("This uses the working JSON endpoint\n")
        import tenderned_json_api_example
        tenderned_json_api_example.main()

if __name__ == "__main__":
    main()
