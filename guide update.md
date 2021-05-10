1. Upgrade Project guide:

	Build docker (docker-compose up --build web)

	Install new libs (pip install -r requirements.txt)

	Run migrate (python manage.py migrate)

	Run collectstatic (python manage.py collectstatic)

2. git guide
	- git commit

	- git pull


	cap nhat: 
	- git pull = git fetch + git merge

	luu tru tam thaY doi:
	- git stash

	dua thay doi da luu:
	- git stash pop

	git add
	git commit

	git reset
	
3. DB
	- su - root
	- CREATE ROLE rolename LOGIN SUPERUSER;
	- CREATE USER admin SUPERUSER; #CREATE USER username SUPERUSER
