<div align='center'>
	<h1>Bandue</h1>
</div>

<br><br>

# Build
`$ docker build -t bandue:bandue .`

# Create Container
`$ docker run -itd -p 8000:8000 -p 8080:8080 --name bandue -v /home/bandue/ bandue:bandue`
