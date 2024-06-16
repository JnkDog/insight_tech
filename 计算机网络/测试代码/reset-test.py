#%%
from scapy.all import *
from random import randint

# 1. 创建一些无效包进行发送
seq_random = randint(1, 65534)
ack_random = randint(1, 65534)
ans, unans = sr(IP(dst='127.0.0.1')/TCP(sport=51109, dport=80, flags='S', seq=seq_random, ack=ack_random))
ans.summary(lambda s:s[1].sprintf("{IP: %IP.src% is alive, TCP: %TCP.flags%}"))

# %%
