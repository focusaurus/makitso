#!/usr/bin/env python
#simplistic and naive and not fancy json query syntax
#It gets the job done and it is very short
import json
import sys


settings = json.load(open(sys.argv[1]))
properties = sys.argv[2].split(".")
properties.reverse()
while properties:
    settings = settings[properties.pop()]
print(settings)
