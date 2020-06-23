<div align='center'>
	<h1>Bandue</h1>
</div>

<br>

# Bandue Start-up
Enter the command in the following procedure

1. Dockerfile Build
`$ docker build -t bandue:bandue .`

2. Create Container
`$ docker run -itd -p 8000:8000 -p 8080:8080 --name bandue -v /home/bandue/ bandue:bandue`

3. Server Start-up
`$ docker exec -it bandue bash`
`$ cd server && python manage.py runserver 0.0.0.0:8000`

4. Client Start-up
`$ docker exec -it bandue bash`
`$ cd client && yarn serve`

5. Redis Start-up
`$ docker run --rm -dp 6379:6379 redis`
