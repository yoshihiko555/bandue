<div align='center'>
	<h1>Bandue</h1>
</div>

<br>

<div align='center'><img src='https://user-images.githubusercontent.com/55835045/85579803-274d6080-b676-11ea-95ff-b8fb4152a8d6.png'></div>

<br>

# Introduction
bandue is a revolutionary communication tool to connect with everyone who makes music

<br>

# Bandue Startup Procedure
Please start by the following procedure

## 1. Docker Install
- [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

## 2. Command Input
Enter the command in the following procedure

1. Dockerfile Build  
`$ docker build -t bandue:bandue .`

2. Create Container  
`$ docker run -itd -p 8000:8000 -p 8080:8080 --name bandue -v <your-volume-path>:/home/bandue/ bandue:bandue`  
※For \<your-volume-path>, enter the directory you want to share with the absolute path

3. Server Start-up  
`$ docker exec -it bandue bash`  
`$ cd server && python manage.py runserver 0.0.0.0:8000`  

4. Client Start-up  
`$ docker exec -it bandue bash`  
`$ cd client && yarn upgrade`  
`$ yarn serve`

5. Redis Start-up  
`$ docker run --rm -dp 6379:6379 redis`

<br>

# Author

[<img src="https://user-images.githubusercontent.com/39425808/84468413-b8592a80-acb9-11ea-8f6a-d962144b2e41.png" width="150px">](https://github.com/kRysTasis)
[<img src="https://user-images.githubusercontent.com/39425808/84468489-eccce680-acb9-11ea-8d16-94b22aa796a1.png" width="150px">](https://github.com/shutotakizawa)
