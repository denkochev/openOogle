1. Install packages

For unix sytem:
```
pip install -r packages.txt
```
For windows:
```
py -m pip install -r packages.txt
```


TO start flask 

 flask --app app_test.py  --debug run --port 5001 


Запуск FastAPI серверу

1. Встановлення пакетів: 
pip install fastapi uvicorn

2. Запуск серверу

For unix sytems:
```
uvicorn app:app --reload
```
For windows:
```
 py -m uvicorn app:app --reload  
```