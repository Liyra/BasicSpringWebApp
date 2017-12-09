#!/usr/bin/python

# Imports
import subprocess, sys, argparse, os
import xml.etree.ElementTree as ET


# Clean and build web app
def Build():
  subprocess.call(["mvn", "clean", "package"], shell=True)


# Deploy on tomcat server
def Deploy():
  subprocess.call(["mvn", "tomcat7:deploy"], shell=True)


# Redeploy on tomcat server
def Redeploy():
  subprocess.call(["mvn", "tomcat7:redeploy"], shell=True)


# Start a tomcat server
def Up():
  subprocess.call([os.environ.get('CATALINA_HOME') + "\\bin\startup"], shell=True)


# Stop a tomcat server
def Down():
  subprocess.call([os.environ.get('CATALINA_HOME') + "\\bin\shutdown"], shell=True)


# Clean, compile and deploy on tomcat server
def Flow():
  Build()
  Redeploy()


# Check environment variables
def checkEnvVar():
  envSetUp = True
  if "CATALINA_HOME" in os.environ:
    pass
  else:
    envSetUp = False
    print('Missing \'CATALINA_HOME\' environment variable!')
  if "JAVA_HOME" in os.environ:
    pass
  else:
    envSetUp = False
    print('Missing \'JAVA_HOME\' environment variable!')
  if "maven" in os.environ.get("PATH"):
    pass
  else:
    envSetUp = False
    print('Missing maven path in the \'PATH\' environment variable!')
  if "tomcat" in os.environ.get("PATH"):
    pass
  else:
    envSetUp = False
    print('Missing tomcat path in the \'PATH\' environment variable!')
  if envSetUp:
    return True
  else:
    return False
    print('You have some invalid environment variables!')


# Prepend for tomcat xml
def prepend_t(s):
    return '{http://tomcat.apache.org/xml}' + s


# Prepend for maven xml
def prepend_m(s):
    return '{http://maven.apache.org/SETTINGS/1.0.0}' + s


# Invalid tomcat xml
def errorTomcat():
  print('It should be <user username="admin" password="password" roles="manager-script"/> in the <tomcat-users> tag')
  return False


# Invalid maven xml
def errorMaven():
  print('It should be <server><id>TomcatServer</id><username>admin</username><password>password</password></server> tag')
  return False


# Check xml config of Maven and Tomcat
def checkXMLConfig():
  rootTomcat = ET.parse(os.environ.get('CATALINA_HOME') + "\\conf\\tomcat-users.xml").getroot()
  for u in rootTomcat.findall(prepend_t('user')):
    if u.get('username') == "admin":
      if u.get('password') == "password":
        if u.get('roles') == "manager-script":
          pass
        else:
          return errorTomcat()
      else:
        return errorTomcat()
    else:
      return errorTomcat()
  pathList = []
  pathString = ''
  for char in os.environ.get('PATH'):
    if char != ';':
      pathString += char
    else:
      pathList.append(pathString)
      pathString = ''
  for path in pathList:
    if 'maven' in path:
      rootMaven = ET.parse(path + "\\..\\conf\\settings.xml").getroot()
      for u in rootMaven.iter(prepend_m('server')):
        if u.find(prepend_m('id')).text == "TomcatServer":
          if u.find(prepend_m('username')).text == "admin":
            if u.find(prepend_m('password')).text == "password":
              pass
            else:
              return errorMaven()
          else:
            return errorMaven()
        else:
          return errorMaven()
  return True

# Checking setup
def Check():
  if checkEnvVar():
    if checkXMLConfig():
      print('Check done, everything\'s good')
    else:
      print('Maven xml file not correctly configured!')
  else:
    print('Set your environment variables!')


# Main
def main(argv):
  parser = argparse.ArgumentParser(description='Script to automatically build and launch this web application')
  sp = parser.add_subparsers(dest='sp')
  sp_build = sp.add_parser('build', help='Clean, build')
  sp_deploy = sp.add_parser('deploy', help='Deploy on a running tomcat server')
  sp_redeploy = sp.add_parser('redeploy', help='Redeploy on a running tomcat server')
  sp_up = sp.add_parser('up', help='Start tomcat')
  sp_down = sp.add_parser('down', help='Stop tomcat')
  sp_flow = sp.add_parser('flow', help='Clean, build, and deploy on a running tomcat server')
  sp_config = sp.add_parser('check', help='Check the environment variables, and the configuration in settings.xml and tomcat-users.xml')
  args = parser.parse_args()
  if args.sp == "build":
    Build()
  if args.sp == "deploy":
    Deploy()
  if args.sp == "redeploy":
    Redeploy()
  if args.sp == "up":
    Up()
  if args.sp == "down":
    Down()
  if args.sp == "flow":
    Flow()
  if args.sp == "check":
    Check()


if __name__ == "__main__":
    main(sys.argv)