#!/usr/bin/env python
from sympy.ntheory import totient
from sympy.ntheory.factor_ import factorint
from math import sqrt
import time

#Based https://securelist.com/blog/research/72097/attacking-diffie-hellman-protocol-implementation-in-the-angler-exploit-kit/
def pohlig_helman(Y, g, p):
	print("Solving 0x%s = 0x%s^x (mod 0x%s)" % (hex(Y), hex(g), hex(p)))
	#print(factorint(p))

	t1 = time.clock()
	n = totient(p)
	t2 = time.clock()
	q = factorint(n)
	t3 = time.clock()

	print("totient(%i) = %i" % (p, n))
	print("factor(%i) = %s" % (n, str(q)))

	print("totient time: " + str(t2-t1))
	print("factor time: " + str(t3-t2))

	t4 = time.clock()
	x_is = list()
	mods = list()
	for p_i in q:
		e = q[p_i]
		
		x_i = solve_xi(Y, g, p, p_i, e, n)
		print("x = %i mod %i" % (x_i, pow(p_i, e)))
		x_is.append(x_i)
		mods.append(pow(p_i, e))
	x = chinese_remainder(mods, x_is)

	t5 = time.clock()

	print("x = %i" % x)
	print("ph time: " + str(t5-t4))

	return x

def solve_xi(Y, g, p, p_i, e, phi):
	p_i = pow(p_i, e)
	H = int(sqrt(p_i)) + 1
	D_a = pow(g, phi/p_i, p)
	D_b = pow(Y, phi/p_i, p)
	D_c = pow(D_a, H, p)
	D_cc = D_c

	part_size = 1000000
	i = 1
	x_i = 0
	while(i <= H):
		table = dict()
		
		for u in range(i, min(H+1, i+part_size)):
			#print("put: %i, %i" % (D_cc, u))
			table[D_cc] = u
			D_cc = (D_cc * D_c) % p 

		z = D_b
		for v in range(0, H+1):
			#print("Z: %i" % z)
			if z in table:
				x_i = (H*table[z] - v) % p_i
				return x_i
			z = (z * D_a) % p
		i += part_size

	return x_i

#source: https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
def chinese_remainder(n, a):
	sum = 0
	prod = reduce(lambda a, b: a*b, n)
 
	for n_i, a_i in zip(n, a):
		p = prod / n_i
		sum += a_i * mul_inv(p, n_i) * p
	return sum % prod
 
#source: https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
def mul_inv(a, b):
	b0 = b
	x0, x1 = 0, 1
	if b == 1: return 1
	while a > 1:
		q = a / b
		a, b = b, a%b
		x0, x1 = x1 - q * x0, x0
	if x1 < 0: x1 += b0
	return x1

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Calculate Angler EK's private key")

	parser.add_argument('-Y', action="store", dest="public", type=int, required=True)
	parser.add_argument('-g', action="store", dest="generator", type=int, required=True)
	parser.add_argument('-p', action="store", dest="modulo", type=int, required=True)

	args = parser.parse_args()
	pohlig_helman(args.public, args.generator, args.modulo)
