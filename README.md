# Subscription Task

---

### What does this program do?
It is a simple service provider.
You can buy whatever service you want and the program
will decrease from your credit automatically.

### Requirements
- Python version 3<br><br>
- Install required packages from `Pipfile` by the following commands:<br>
`$ pipenv install`<br><br>
- If the virtualenv is already activated, you can also use:<br>
`$ pipenv sync`<br><br>
- To install by `requirements.txt` file:<br>
`$ pip install -r /path/to/requirements.txt`


### Usage
First, program needs a secret key to be able to run. Create a file called `.env` in `src/authentication` folder, 
and make an environment variable called `SECRET_KEY` in the file. For example:<br>
`SECRET_KEY = "your secret key"`<br><br>
Create your secret key by one of th following ways:
- Use `secrets` python library:<br>
    In python shell, import secrets and run this method `secrets.token_hex()`
- Use terminal and run `openssl rand -hex 32`<br><br>
Run `main.py` file in `src` folder by the following command:<br>
`$ python main.py` or `$ python3 main.py`<br>
Make sure you are in `src` folder.
Open a browser and browse `http://localhost:8000` url.

### Document
See `docs` folder for documents and diagrams.