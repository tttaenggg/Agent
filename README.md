# Agent
## Installation guide.
 **1.Clone Volltron branch dev**
    > git clone .... --branch develop
 
 **2.Follow Installation Guide**
 
 **3. Clone Agent Reposity**
 - Becareful :
     - project Tree look like :
     `~\workspace\platform-name\volttron\Agent`
 
 ![alt text](https://github.com/Soulweed/Agent/blob/master/tree.png)
 
 **5 setup env
 
  ![alt text](https://i.ibb.co/j3YqQXj/2020-03-04-19-30-27.jpg)
 
 
 
 **6. After Clone Agent Folder**
 
 - cd into > ../volttron/Agent/
 
 - > pip install -r requirement.txt
 
 **7 build agent 
 
 python scripts/install-agent.py -s Agent/ListenerAgent/ -c Agent/ListenerAgent/config -t listener_agent --start


