#!/usr/bin/env python
    
from magi.util.agent import DispatchAgent, agentmethod
from magi.util.execl import run, pipeIn
from magi.util.processAgent import initializeProcessAgent

import errno
import logging
import os
import glob
import stat
import time
import re
import StringIO
import sys
import subprocess
import tempfile
import threading
import xmlrunner
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import DeterLabTesting

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# the getAgent() method must be defined somewhere for all agents.
# The Magi daemon invokes this mehod to get a reference to an
# agent. It uses this reference to run and interact with an agent
# instance.
def getAgent(**kwargs):
    agent = node0()
    agent.setConfiguration(None, **kwargs)
    return agent


class node0(DispatchAgent):
    def __init__(self):
        DispatchAgent.__init__(self)
        # usually replaced by an "arg" from the agent
        self.report_dir = "/tmp"

    @agentmethod()
    def test003(self, msg):
        log.info("About to start unit tests...")
        log.info(" ... writing test results to: " + self.report_dir)
        print("Testing stdout!")
        try:
            stream = StringIO.StringIO()
            suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
            xmlrunner.XMLTestRunner(stream=stream, output=self.report_dir).run(suite)
            stream.seek(0)
            log.info(stream.read())
        except Exception, err:
            log.exception(err)
        log.info("Done with the unit tests")


class Tests(unittest.TestCase):


    def test003_reachability_node1(self):
        dtl = DeterLabTesting.DeterLabTesting()
        rc, msg, loss = dtl.ping("node-1")
        if rc != 0 or loss > 0:
            self.fail(msg)
        pass


    def test003_reachability_node2(self):
        dtl = DeterLabTesting.DeterLabTesting()
        rc, msg, loss = dtl.ping("node-2")
        if rc != 0 or loss > 0:
            self.fail(msg)
        pass


    def test003_reachability_node3(self):
        dtl = DeterLabTesting.DeterLabTesting()
        rc, msg, loss = dtl.ping("node-3")
        if rc != 0 or loss > 0:
            self.fail(msg)
        pass
    

    def test003_reachability_node4(self):
        dtl = DeterLabTesting.DeterLabTesting()
        rc, msg, loss = dtl.ping("node-4")
        if rc != 0 or loss > 0:
            self.fail(msg)
        pass
    

    def test003_reachability_outside(self):
        dtl = DeterLabTesting.DeterLabTesting()
        rc, msg, loss = dtl.ping("128.9.128.127")
        if re.search("Destination Host Unreachable", msg, re.MULTILINE) is None:
            self.fail(msg)
        pass
   
    
    def test003_bw_node1_100mb(self):
        dtl = DeterLabTesting.DeterLabTesting()
        rc, msg, dtl.bw_mb = dtl.bw("node-1")
        if rc != 0 or dtl.bw_mb < 80 or dtl.bw_mb > 105:
            self.fail(msg)
        pass



# allow the test to be run by hand for development
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)


