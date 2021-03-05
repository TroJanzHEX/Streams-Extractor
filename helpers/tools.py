#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import os
import shlex
import asyncio

from typing import Tuple


async def execute(cmnd: str) -> Tuple[str, str, int, int]:
    cmnds = shlex.split(cmnd)
    process = await asyncio.create_subprocess_exec(
        *cmnds,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)

async def clean_up(input1, input2=None):
    try:
        os.remove(input1)
    except:
        pass
    try:
        os.remove(input2)
    except:
        pass        