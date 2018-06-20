# Summer Python Internship for Skygate
### Usage
###### Clone it
`$ mkdir folder_name & cd folder_name`<br>
`$ git clone https://github.com/b1oader/intern_18.git`
###### Virtual Environment [pip is needed]
install<br>
`$ pip install virtualenv`<br>
create<br>
`$ python -m venv your_venv_name`<br>
run<br>
`$ your_venv_name\Scripts\activate`<br>
###### Upgrade pip
`$ python -m pip install --upgrade pip`<br>
###### Requirements
`$ pip install -r requirements.txt`<br>
###### Migrations & runserver
`$ python manage.py makemigrations`<br>
`$ python manage.py migrate`<br>
`$ python manage.py runserver`<br>
###### Tests
`$ python manage.py test saakar`<br>
### API endpoints
#### Heroes ranking [READ][EVERYONE]
###### List
/GlobalRanking/
#### Dead heroes ranking [READ][ADMIN]
###### List
/DeadHeroes/
#### Type [CRUD][ADMIN]
###### List
/Type/
###### Detail
/Type/[id]
#### Hero [CRUD][ADMIN]
###### List
/Hero/
###### Detail
/Hero/[id]
#### Fight [CREATE READ DELETE][ADMIN]
###### List
/Fight/
###### Detail
/Fight/[id]
<br>
### Admin panel
/admin/
<br>
