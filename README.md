# Virtualization Evaluation System
ves: web version used to test the virtual machine and physical machine's performance

## Dependencies
```sh
pip install django==1.7 mysql-python
```

## Configure
update your mysql configuration in ./virtualization_evaluation/database.py first 
```sh
vim virtualization_evaluation/database.py
./bootstrap
```

## Usage
```sh
python manage.py runserver 0.0.0.0:80
```
