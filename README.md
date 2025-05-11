# pingmon-www
While teaching network/firewall classes at work, I had a need for a simple up/down detector/indicator.  All of the standard options were too heavy for my needs.  So I set out to develop a simple dockerized ping checker with simple web red/green target status.  That's it.  No alerting, no history, no integrations, etc.

I'm not making this available in order to fit your niche, but if it does, GREAT!.  My real motivation for making this available is in the hopes that should you travel down this same path, that you will find this and it might help you along in your learning journey.  I know I would have appreciated such.

1). git clone https://github.com/nf9k/pingmon-www.git  
2). cd ./pingmon-www  
3). `docker build -t nf9k/pingmon-www:latest .` -or- `docker pull nf9k/pingmon-www:latest`  
4). Edit targets.yaml as needed  
5). `docker run -p 5000:5000 -v ./targets.yaml:/app/targets.yaml nf9k/pingmon-www:latest`  
6). visit http://loalhost:5000 for status page

Changes to targets.html will be detected automatically, no need to stop/restart container.
