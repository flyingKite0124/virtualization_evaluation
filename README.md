# Virtualization Evaluation System
ves: web version used to test the virtual machine and physical machine's performance

## Dependencies
```sh
pip install django==1.7
```

## Configure
update your mysql configuration in /virtualization_evaluation/database.py first 
```sh
./bootstrap
```

## Usage
```sh
python manage.py runserver 0.0.0.0:80
```
