# -*- coding: utf-8 -*-
from Queue import Queue
import os
import sys
import signal
from time import sleep
from core import config
from core.process import LogProducer, LogConsumer
from libs.parser import Parser


__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class State(object):
    terminated = False
state = State()


class UtkSystem(object):
    """
    Represent the complete usertk system
    """

    def __init__(self):
        super(UtkSystem, self).__init__()

    def __test_status(self):
        """Test if the system is running and return his PID.

        It will create the PID file if not exists
        """
        # get a logger for debug
        l = config.LOGGER
        if os.path.exists(config.PID):
            fpid = open(config.PID, 'r')
        else:
            fpid = open(config.PID, 'w')
            fpid.write("0\n")
            fpid.close()
            fpid = open(config.PID, 'r')
            l.warning("The PID file don't exists on {0} recreating it".format(
                config.PID
            ))
        pid = long(fpid.readline().split()[0])
        fpid.close()
        if os.path.exists("/proc/%d" % (pid,)):
            l.debug("The system is running with PID: {0}".format(pid))
            return pid

        l.debug("The system is not running")
        return False

    @staticmethod
    def signal_handler(signum, frame):
        l = config.LOGGER
        if signum == signal.SIGUSR1:
            l.debug('Got SIGUSR1 exiting')
            UtkSystem.true_stop()
            sys.exit(0)

    def do_fork_and_run(self):
        l = config.LOGGER
        child_pid = os.fork()
        if child_pid == 0:
            # we are in the chield process, well done
            # install signal handler
            signal.signal(signal.SIGUSR1, UtkSystem.signal_handler)
            if signal.getsignal(signal.SIGUSR1) == UtkSystem.signal_handler:
                l.warning("Usertk started with PID: %d", os.getpid())
                self.run()
            else:
                l.error("Could't install signal handler")
                sys.exit(1)
        else:
            # the fork is done and we have the child_pid, we must update
            # the PID file and exit
            fpid = open(config.PID, 'w')
            fpid.write("%d\n" % (child_pid,))
            fpid.close()

        sys.exit(0)

    def start(self):
        """
        Start the usertk system
        """
        if not self.__test_status():
            # if the system is not running start it
            self.do_fork_and_run()
        else:
            # notify directly to the user, this will print directly to
            # the console.
            print "Usertk is already running."

    @staticmethod
    def load_plugins():
        """Try to import all installed pluggins"""
        try:
            for p in config.PLUGS:
                # TODO: is this the way to do it?
                __import__(p)
        except Exception, e:
            config.LOGGER.debug("Error loading plugin: %s", p)
            config.LOGGER.debug("Error message: %s", e)
            sys.exit(1)

    @staticmethod
    def true_stop():
        """
        Stop log processing
        """
        state.parser.closeOperations()
        state.q.join()
        config.LOGGER.debug("Terminated")

    def stop(self):
        pid = self.__test_status()
        if pid:
            os.kill(pid,signal.SIGUSR1)
            while self.__test_status():
                config.LOGGER.debug("Waiting for the system to exit")
                sleep(3)
            os.unlink(config.PID)
        else:
            config.LOGGER.debug("Usertk is not running")
        sys.exit(0)

    @staticmethod
    def run():
        """Enter the running state"""
        UtkSystem.load_plugins()
        state.q = Queue(maxsize=5)
        state.parser = Parser(config.SQUID_ACCESS_LOG)
        state.p = LogProducer(state.q, state.parser)
        state.c = LogConsumer(state.q)
        #start all threads
        state.c.start()
        config.LOGGER.debug("Started consumer thread")
        state.p.start()
        config.LOGGER.debug("Started producer thread")
        # wait until all log entrys are processed
        config.LOGGER.debug("Processing started")
        state.q.join()
