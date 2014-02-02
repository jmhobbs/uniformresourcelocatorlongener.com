#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from flask.ext.script.commands import Clean, ShowUrls

from urllongener import app

manager = Manager(app)
manager.add_command("clean", Clean())
manager.add_command("urls", ShowUrls())

if __name__ == "__main__":
    manager.run()
