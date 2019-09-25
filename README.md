# Remote Downloader

Web tool made with Flask for queuing direct downloads remotely.  
This tool was made for a personal usage originaly but feel free to use and modify it !

## Installation

Create a virtual environment.

```bash
python -m venv venv
. venv/bin/activate
```

Use [pip](https://pip.pypa.io/en/stable/) to install all the requirements in `requirements.txt`.

```bash
pip install -r requirements.txt
```

Edit `variables.py` to use your desired parameters (ie. default port is `5000`)

## Usage

First launch the Flask server

```bash
. venv/bin/activate
python app.py
```
then access the frontend on `http://localhost:5000/` or using your public ip.