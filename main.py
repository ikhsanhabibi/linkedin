import indeed, linkedin, simplyhired

bots = ['indeed','linkedin', 'simplyhired']

modules = map(__import__, bots)

import multiprocessing

multiprocessing.Process(target=modules)