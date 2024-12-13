# CRM Tinkerer CLI

This is an CLI for Homeworld modding tools by Russian modding community CRM.\
It can be used as standalone CLI or embedded with higher level software.

> ***Why using portable Winpython?***
> 
> We want this tool to be simple, portable and easy to use by non-programmers.\
> You can remove python folder if you are planning to use CLI as standalone solution with your own interpreter. 

## Capabilities

### DevMode

Replaces some script values with lower numbers or restores them to original from cache if devmode is already enabled.\
Script values to be changed:\
• def_research.lua for all races, except evo and random, Cost and Time values.\
• ships files, buildCost and buildTime.
• subs files, costToBuild, timeToBuild.


## Usage

### DevMode

#### Use Devmode from command line:
```
python-3.12.6.amd64\python.exe cli devmode [Source]
```
#### Or just drop a source folder to drop_devmode.bat
