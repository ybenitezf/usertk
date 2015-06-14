# -*- coding: utf-8 -*-
__author__ = 'http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/'

import sys, os, time, atexit
import signal


class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, logger, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.logger = logger

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        l = self.logger
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            l.debug("fork #1 failed: %d (%s)", e.errno, e.strerror)
            sys.exit(1)

        l.debug("fork #1 success")

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            l.debug("fork #2 failed: %d (%s)", e.errno, e.strerror)
            sys.exit(1)

        l.debug("fork #2 success")

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        l.debug("Deamon stated with PID: %s", pid)
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        self.logger.debug("Cleanning up")
        self.cleanup()
        # os.remove(self.pidfile)

    def cleanup(self):
        """
        Do the clean up
        """
        pass

    def status(self):
        """Test if the system is running and return his PID.

        It will create the PID file if not exists
        """
        # get a logger for debug
        l = self.logger
        if os.path.exists(self.pidfile):
            fpid = open(self.pidfile, 'r')
        else:
            fpid = open(self.pidfile, 'w')
            fpid.write("0\n")
            fpid.close()
            fpid = open(self.pidfile, 'r')
            l.warning("The PID file don't exists on {0} recreating it".format(
                self.pidfile
            ))
        pid = long(fpid.readline().split()[0])
        fpid.close()
        if os.path.exists("/proc/%d" % (pid,)):
            l.warning("The system is running with PID: {0}".format(pid))
            return pid

        l.debug("The system is not running")
        return False

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        l = self.logger
        if not self.status():
            l.debug("Entering deamon state")
            self.daemonize()
            l.debug("Entering running state")
            self.run()
        else:
            sys.exit(1)

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        l = self.logger
        pid = self.status()

        if not pid:
            # not running
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            l.debug("Sending signal.SIGTERM to PID: %d", pid)
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                l.debug(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        raise NotImplementedError()
