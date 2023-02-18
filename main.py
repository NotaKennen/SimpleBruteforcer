from itertools import chain, product
from random import sample
from string import ascii_letters, digits, punctuation, whitespace
import time
import psutil
import os

################### Config
password = input(str("Input the password you want to crack? >>> "))
limit_cpu_usage = True

################### Code
t0 = time.time()
print("Cracking the password...")

def limit_cpu():
    "is called at every process start"
    p = psutil.Process(os.getpid())
    # set to lowest priority, this is windows only, on Unix use ps.nice(19)
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

def brute(start_length=1, length=20, ramp=True, letters=True, numbers=True, symbols=False, spaces=False):
    choices = ''
    choices += ascii_letters if letters else ''
    choices += digits if numbers else ''
    choices += punctuation if symbols else ''
    choices += whitespace if spaces else ''
    choices = ''.join(sample(choices, len(choices)))

    if ramp:
        if start_length < 1 or start_length > length:
            start_length = 1

    return (
        ''.join(candidate) for candidate in
        chain.from_iterable(product(choices, repeat=i) for i in range(start_length if ramp else length, length+1))
    )

if limit_cpu_usage == True:
    limit_cpu()

oldlen = 0
for s in brute():
    if s == password:
        status = True
        break
    if len(s) > oldlen:
        t2 = time.time()
        print(f"Trying {len(s)} letter passwords, {round(t2-t0, 2)} seconds passed.")
        oldlen = len(s)

t1 = time.time()

total = t1-t0
if total >= 120:
    units = "minutes"
    total = total / 60
else:
    round(total, 3)
    units = "seconds"

################### Output

print("----------------")
if status == True:
    print(f"Password has been found!\nPassword is: {s}\nCracking took {total} {units}.")
else:
    print("The password wasn't found, try increasing length or changing parameters")
print("----------------")