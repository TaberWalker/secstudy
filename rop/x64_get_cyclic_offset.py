#!/usr/bin/env python
# coding=utf-8

import os
from pwn import *


context.clear()
context.update(arch='x86_64', os='linux', endian='little', word_size=64)
context.log_level = 'debug'
log.info(vars(context))


# generate core
io = process('./a.out')
io.sendline(cyclic(1024))
io.recvall()
pid = io.pid
log.debug('core pid = ' + str(pid))

# get cyclic offset from core file
# echo "core.%p" > /proc/sys/kernel/core_pattern
core_filename = 'core.' + str(pid)
core = Core(core_filename)
rsp = core.rsp
log.debug('rsp = ' + hex(rsp))
cyclic_value = core.u32(core.rsp)
log.debug('cyclic_value = ' + hex(cyclic_value))
cyclic_offset = cyclic_find(cyclic_value)
log.info('cyclic_offset = ' + str(cyclic_offset))

# remove core file
os.remove(core_filename)

