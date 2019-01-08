#!/usr/bin/env python

import os
import sys
import pdfrw
import pprint
import re
import json

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

"""
{
    '/Border': ['0', '0', '0'],
    '/Rect': ['49.08', '693.509', '184.17', '708.854'],
    '/T': '(city)',
    '/F': '4',
    '/BS': (2429, 0),
    '/Subtype': '/Widget',
    '/DA': '(/TimesNewRomanPSMT 10 Tf 0 g)',
    '/MK': (2430, 0),
    '/TU': '(City)',
    '/AP': (2431, 0),
    '/StructParent': '626',
    '/V': '(Chicago)',
    '/FT': '/Tx',
    '/Type': '/Annot',
    '/Ff': '8388608',
    '/DR': (2432, 0)
}
"""

int_fields = {
    'num_initiation'
}

float_fields = {
    'amount_initiation',
    'amount_regular_stamps',
    ''
}

delegate_report = pdfrw.PdfReader(sys.argv[1])
report_data = {}
member_information_changes = {}
dues_collections = {}

for page in delegate_report.pages:
    annotations = page[ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            key = annotation[ANNOT_FIELD_KEY]
            value = annotation[ANNOT_VAL_KEY]
            if key and value:
                key = key.strip('()')
                value = value.strip('()')
                if key and value:
                    if value == '/Yes':
                        value = True
                    if value == '/No':
                        value = False
                    if re.match('^num_', key):
                        value = int(value)
                    elif re.match('^amount_', key) or re.match('^totals', key):
                        value = float(value)
                    elif re.match('^changes_', key):
                        changes_key = re.search('changes_(.*)_\d+', key).group(1)
                        try:
                            member_information_changes[int(key[-1]) - 1][changes_key] = value
                        except KeyError as e:
                            member_information_changes[int(key[-1]) - 1] = {}
                            member_information_changes[int(key[-1]) - 1][changes_key] = value
                        continue
                    report_data[key] = value
                    report_data['member_information_changes'] = [member_information_changes[i] for i in member_information_changes.keys()]

print(json.dumps(report_data))

