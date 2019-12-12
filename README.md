pyml
====

Python as YAML proof-of-concept. Maybe don't use this for anything serious.

See https://twitter.com/akx/status/1205118662421762048

Usage
-----

Convert Python to YAML:

```
python pyml.py -d calc_example.py > calc_example.pyml
```

Execute YAML as Python:

```
python pyml.py -x calc_example.pyml
```
