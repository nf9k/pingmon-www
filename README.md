# pingmon-www
Simple dockerized ping checker with simple web red/green target status.

1). git clone https://github.com/nf9k/pingmon-www.git
2). cd ./pingmon-www.git

3a). docker build . 
	-or- 
3b). docker pull nf9k/pingmon-www:latest

4). Edit targets.yaml as needed
5). docker run -p 5000:5000 -v ./targets.yaml:/app/targets.yaml nf9k/pingmon-www:latest
6). visit http://loalhost:5000 for status page

Changes to targets.html will be detected automatically, no need to stop/restart container.
