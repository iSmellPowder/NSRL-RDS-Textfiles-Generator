# RDSv3 to RDS 2.XX Format Text Files
Python script to generate the RDS v2 format text files given a RDS v3 database file

This entire script is just a python translation of the instructions given [here](https://s3.amazonaws.com/rds.nsrl.nist.gov/RDS/RDSv3_Docs/RDSv3_to_RDSv2_text_files.pdf).

## Pre-requisites
1. NSRL RDSv3 Minimal Set.  Download the latest RDS [here](https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds).

      **NOTE:** This script is only works on minimal sets (modern PC, legacy PC, android, iOS)

      **NOTE:** Extract the .db file, and duplicate it before using script. (In case something went wrong, you don't have to re-download .db file again)

2. Python3 

## Usage
- **IMPORTANT** Change `PRAGMA cache_size = ` in `generate_NSRLFile()` to a **maximum** of 50% of your total RAM (e.g. 32GB RAM, use only 16GB)
  - Your computer may crash if you do not change this
  - The other `PRAGMA cache_size = ` in the code you can leave it as it is
  
- `python NSRLv3_Textfiles_Generator.py` and follow on screen instructions

## Note
- `generate_NSRLFile` is extremely resource intensive. It is highly recommended to close all memory-intensive applications (I'm looking at you, chrome) before executing this process

## Bugs
Please create a ticket here and I'll look into it. Or, you can always solve it yourself ;) 
