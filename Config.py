#!/usr/bin/python

import getopt
import sys
import os
import logging

from ConfigParser import *

class Config():
   def __init__(self):
       self.debug = 0
       self.output_filename = "/dev/null"
       self.hostname = "127.0.0.1"
       self.port = 4001
       self.username = "admin"
       self.password = ""
       self.config = None
       self.dbhost = "127.0.0.1"
       self.dbname = "donkeysurvey"
       self.dbuser = "donkeysurvey"
       self.dbpass = "donkeysurvey"

   def usage(self):
       print "Syntax error"
       print "  -h, --help           This help"
       print "  -d, --debug          Set debug to true. Default is false."
       print "  -o, --output=FILE    Dump all output in FILE. (Default is Stdout)"
       print "  -H, --host=HOST      Host name to connect. (Default is 127.0.0.1)"
       print "  -p, --port=PORT      Port to connect. (Default is 4001)"
       print "  -U, --user=USER      User for authentication. (Default is admin)"
       print "  -P, --pass=PASS      Password for authentication. (Default is empty)"
       print "  -D, --dbhost=HOST    Host name for database connection. (Default is 127.0.0.1)"
       print "  -N, --dbname=DBNAME  Database name for store data. (Default is donkeysurvey)"
       print "  -u, --dbuser=DBUSER  Database username for store data. (Default is donkeysurvey)"
       print "  -w, --dbpass=DBPASS  Database password for store data. (Default is donkeysurvey)"

   def read_option(self, section, option):
       var = "self.%s" % option
       if self.config.has_option(section, option):
           return self.config.get(section, option)
       else:
           return eval(var)
      
   def load_options(self):
       try:
           self.config = ConfigParser()
           self.config.read(['/etc/donkeysurvey/donkeysurvey.conf', 
                             os.path.expanduser('~/.donkeysurveyrc')])
       except (MissingSectionHeaderError), err:
           logging.error("Error in config file syntax: %s", str(err))
           sys.exit(2)
 
       self.debug = self.read_option('general', 'debug')
       self.output_filename = self.read_option('general', 'output_filename')
       self.hostname = self.read_option('mldonkey', 'hostname')
       self.port = self.read_option('mldonkey', 'port')
       self.username = self.read_option('mldonkey', 'username')
       self.password = self.read_option('mldonkey', 'password')
       self.dbhost = self.read_option('database', 'dbhost')
       self.dbname = self.read_option('database', 'dbname')
       self.dbuser = self.read_option('database', 'dbuser')
       self.dbpass = self.read_option('database', 'dbpass')

       short_options = "hdo:H:p:U:P:D:N:u:w:"
       long_options = ["help", "debug", "output=", "host=", 
                       "port=", "user=", "pass=", "dbhost=", "dbname=", "dbuser=", "dbpass="]
       try:
           opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
       except getopt.GetoptError, err:
           logging.error("Error parsing args: %s", str(err))
           self.usage()
           sys.exit(2)

       for o, a in opts:
           if o in ("-h", "--help"):
               self.usage()
               sys.exit(0)
           elif o in ("-d", "--debug"):
               self.debug = 1
           elif o in ("-o", "--output"):
               self.output_filename = a
           elif o in ("-H", "--host"):
               self.hostname = a
           elif o in ("-p", "--port"):
               self.port = int(a)
           elif o in ("-U", "--user"):
               self.username = a
           elif o in ("-P", "--pass"):
               self.password = a
           elif o in ("-D", "--dbhost"):
               self.dbhost = a
           elif o in ("-N", "--dbname"):
               self.dbname = a
           elif o in ("-u", "--dbuser"):
               self.dbuser = a
           elif o in ("-w", "--dbpass"):
               self.dbpass = a
           else:
               assert False, "unhandled option"
