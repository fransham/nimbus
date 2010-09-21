import string
import random
import os
import sys
import nose.tools
import boto
from boto.ec2.connection import EC2Connection
import boto.ec2 
import sys
from ConfigParser import SafeConfigParser
import time
import unittest
import tempfile
import filecmp
import pycb
import pynimbusauthz
from  pynimbusauthz.db import * 
from  pynimbusauthz.user import * 
import pycb.test_common
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
import random
from nimbusweb.setup.groupauthz import *
import nimbus_public_image

def get_nimbus_home():
    """Determines home directory of Nimbus install we are using.
    
    First looks for a NIMBUS_HOME enviroment variable, else assumes that
    the home directory is the parent directory of the directory with this
    script.
    """
    nimbus_home = os.getenv("NIMBUS_HOME")
    if not nimbus_home:
        script_dir = os.path.dirname(__file__)
        nimbus_home = os.path.dirname(script_dir)
    if not os.path.exists(nimbus_home):
        raise CLIError('ENIMBUSHOME', "NIMBUS_HOME must refer to a valid path")
    return nimbus_home


class TestEC2Submit(unittest.TestCase):

    def killall_running(self):
	instances = self.ec2conn2.get_all_instances()
        print instances
        for reserv in instances:
            for inst in reserv.instances:
                if inst.state == u'running':
                    print "Terminating instance %s" % inst
                    inst.stop()


    def cb_random_bucketname(self, len):
        chars = string.letters + string.digits
        newpasswd = ""
        for i in range(len):
            newpasswd = newpasswd + random.choice(chars)
        return newpasswd

    def _make_user(self):
        fn = str(uuid.uuid1())
        self.can_user2 = User(self.db, friendly=fn, create=True)
        self.subject2 = self.cb_random_bucketname(21)
        self.s3id2 = self.cb_random_bucketname(21)
        self.s3pw2 = self.cb_random_bucketname(42)
        self.s3user2 = self.can_user2.create_alias(self.s3id2, pynimbusauthz.alias_type_s3, fn, self.s3pw2)
        self.dnuser2 = self.can_user2.create_alias(self.subject2, pynimbusauthz.alias_type_x509, fn)


    def setUp(self):
        host = 'localhost'
        cumport = 8888
        ec2port = 8444
        self.db = DB(pycb.config.authzdb)

        self._make_user()

        self.ec2conn2 = EC2Connection(self.s3id2, self.s3pw2, host=host, port=ec2port, debug=2)
        self.ec2conn2.host = host

        cf = OrdinaryCallingFormat()
        self.s3conn = S3Connection(self.s3id2, self.s3pw2, host=host, port=cumport, is_secure=False, calling_format=cf)
        self.db.commit()
        self.killall_running()

    def tearDown(self):
        if self.s3user2 != None:
            self.s3user2.remove()
        if self.dnuser2 != None:
            self.dnuser2.remove()
        if self.can_user2 != None:
            self.can_user2.destroy_brutally()
        if self.db != None:
            self.db.close()
        self.killall_running()

    def test_upload_delete_common(self):
        image_name = str(uuid.uuid1())
        rc = nimbus_public_image.main(["/etc/group", image_name])
        self.assertEqual(rc, 0, "public image upload return code should be 0 is %d" % (rc))
        rc = nimbus_public_image.main(["--delete", image_name])
        self.assertEqual(rc, 0, "public image upload return code should be 0 is %d" % (rc))

    def test_run_common(self):
        image_name = str(uuid.uuid1())
        rc = nimbus_public_image.main(["/etc/group", image_name])
        self.assertEqual(rc, 0, "public image upload return code should be 0 is %d" % (rc))

        image = self.ec2conn2.get_image(image_name)
        res = image.run()
        res.stop_all()

        rc = nimbus_public_image.main(["--delete", image_name])
        self.assertEqual(rc, 0, "public image upload return code should be 0 is %d" % (rc))
