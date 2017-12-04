# -*- coding:utf-8 -*-
import os
import sys
from subprocess import call
from functools import partial
from argparse import ArgumentParser

call = partial(call, stderr=sys.stdout, stdout=sys.stdout)

cmds = [
    "docker build -f docker/%s.dockerfile -t 192.168.200.51/longen/%s:latest .",
    "docker push 192.168.200.51/longen/%s"
    ]


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--message", default="auto commit")
    parser.add_argument("services", nargs="+", help="service")
    args = parser.parse_args()
    result = True
    for service in args.services:
        result = result and deploy(service)
        if not result:
            return
    if result:
        call(["git", "commit", "-a", "-m", args.message])
        call(["git", "push"])


def deploy(service):
    for cmd in cmds:
        if call((cmd%tuple([service]*cmd.count("%s"))).split(" ")):
            return False
    return True


if __name__ == "__main__":
    main()