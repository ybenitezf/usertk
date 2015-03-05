# -*- coding: utf-8 -*-
__author__ = 'Yoel Benitez Fonseca <mark@grm.uci.cu>'

import re


class Excludes(object):

    def __init__(self, filename):
        """
        Read filename and create list of RE for exclutions
        """
        f = open(filename)
        self.relist = list()
        for line in f:
            line = line.strip("\n")
            if line.startswith(';'):
                # ignore comments
                continue
            elif not line:
                # ignore blank lines
                continue
            self.relist.append(re.compile(line))
        f.close()

    def is_exclude(self, uri):
        """
        Returns True if it finds a mach in URI for an exclude
        """
        for r in self.relist:
            match = r.findall(uri)
            if len(match):
                return True

        return False
