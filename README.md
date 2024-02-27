# SLR Helpers

## Usage

On Linux/macOS (hereby Linux) use `bash`/`zsh`  
On Windows use ~linux~ `powershell`

Ensure `Python 3` is installed

### Enable the environment
Needs to be done once per terminal

**Linux**
```sh
source venv/bin/activate
```

**Windows**
```sh
venv/bin/Activate.ps1
```

### To run the golden standard comparison
```sh
python src/main.py -gs golden/GoldenStandardsDOI.xlsx -o output/results.xlsx -i input/scopus.bib
```
The inputs can take a list of inputs which will each get a column in the results.  
Just replace the `scopus.bib` with a space separated list of `.bib` files.  

> `.bib` is used as it is supported and standardized across most sites and tools.
> `.xlsx` is supported for excel, more formats can be added later.

## How to Install

Requires `python3`
Go to the directory of the repository

**Linux**
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows**
```sh
python3 -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv/bin/Activate.ps1
pip install -r requirements.txt
```
For more info on python [virtual environment](https://docs.python.org/3/library/venv.html)

