# Requirements
import json

req = [
    "requests==2.32.3",
    "pyramid==2.0.2",
    "pyyaml==6.0.1",
    "pyramid_urireferencer==0.8.0",
]

# Dev Requirements
dev_req = [
    "sphinx==7.3.7",
    "sphinxcontrib-httpdomain==1.8.1",
    "sphinxcontrib-plantuml==0.30",
    "waitress==3.0.0",
    "pyramid_debugtoolbar==4.12.1",
    "pytest==8.2.2",
    "pytest-cov==5.0.0",
    "webtest==3.0.0",
    "httpretty==1.1.4",
    "coveralls==4.0.1",
]

print(json.dumps(sorted(req), indent=4, sort_keys=True))
print(json.dumps(sorted(dev_req), indent=4, sort_keys=True))
