1. Install packages

For unix sytem:
```
pip install -r packages.txt
```
For windows:
```
py -m pip install -r packages.txt
```

2. To work with this backend you have to install PosgreSQL on your machine. Then set 
your configuration variables (user, password) in credentials.py file.


3. Launch backend.

For unix sytems:
```
uvicorn app:app --reload
```
For windows:
```
 py -m uvicorn app:app --reload  
```

