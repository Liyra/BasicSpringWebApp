## BasicSpringWebApp

This is a basic Spring web application in java build from scratch with Intellij, with Maven and Bootstrap.
The dependancies are Maven (I used 3.5.2) and Tomcat (I used 8.5.24).

The script.py file is a script allowing quicker deployment on tomcat. It has a check option where it tells you what step you forgot (ie. environment variables not set up). This script should work only on windows.

### Setup

In order to make it run smoothly, you need to edit the tomcat-users.xml file in your tomcat installation to add:
```
<user username="admin" password="password" roles="manager-script"/>
```
And you need to edit the settings.xml of your maven installation to add:
```
<server>
  <id>TomcatServer</id>
  <username>admin</username>
  <password>password</password>
</server>
```
Launch tomcat (script.py up), build and deploy (script.py build, script.py deploy), and the website should display itself at localhost:8080. (You can obviously use the traditionnal maven and tomcat commands)

### Rights

The frontend is based on templates, https://html5up.net/aerial for the main page (LICENSE_index_theme.txt and README_index_theme.txt) and the example of carousel from the Bootstrap documentation https://getbootstrap.com/docs/4.0/components/carousel/.

The images are labeled for reuse (from publicdomainpictures.net and wikipedia.org).
