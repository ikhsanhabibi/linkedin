import indeed, linkedin

bots = ['indeed','linkedin']

modules = map(__import__, bots)

import multiprocessing

multiprocessing.Process(target=modules)