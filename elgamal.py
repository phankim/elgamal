import random
import math

n = 0
t = 0

# computes the greatest common denominator of a and b.  assumes a > b
def gcd( a, b ):
	if b != 0:
		return gcd( b, a % b )
	#returned if b == 0
	return a	
	
#computes base^exp mod modulus
def modexp( base, exp, modulus ):
	if exp == 0:
		return 1

	temp = exp
	if temp < 0:
		temp = math.ceil(temp/2)
	else:
		temp = temp / 2 
	
	z = modexp( base, temp, modulus )

	if exp % 2 == 0:
		return z*z % modulus
	else:
		return base*z*z % modulus

#solovay-strassen primality test.  tests if n is prime
def SS( num ):
	f = open('count', 'w')
	for i in range(t):
		#choose random a between 1 and n-2
		a = random.randint( 1, num-1 )
		
		#if a is not relatively prime to n, n is composite
		if gcd( a, num ) > 1:
			f.write( 'fuck' )
			return False
		
		#declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
		if not jacobi( a, num ) == modexp ( a, (num-1)/2, num ):
			f.write( 'shit' )
			return False
		f.close()
	return True

#computes the jacobi symbol of a, n
def jacobi( a, n ):
	if a == 0:
		if n == 1:
			return 1
		else:
			return 0
	elif a == -1:
		return -1**((n-1)/2)
	elif a == 1:
		return 1
	elif a == 2:
		return -1**(((n**2)-1)/8)
	elif a >= n:
		return jacobi( a%n, n)
	elif a%2 == 0:
		return jacobi(2, n)*jacobi(a/2, n)
	else:
		if a % 4 == 3 and n%4 == 3:
			return -1 * jacobi( n, a)
		else:
			return jacobi(n, a )





	if False:
		#property 1 of the jacobi symbol
		if a == -1:
			return (-1)**((n-1)/2)
		#if a == 1, jacobi symbol is equal to 1
		elif a == 1:
			return 1
		#property 1 of the jacobi symbol
		#if a = b mod n, jacobi(a, n) = jacobi( b, n )
		elif abs(a) > abs(n):
			z = jacobi( a % n, n )	
		#property 4 of the jacobi symbol
		elif a == 2:
			return (-1)**(((n**2)-1)/8)
		#law of quadratic reciprocity
		#if a is odd and a is coprime to n
		elif a % 2 == 1 and gcd( a, n ) == 1:
			if a % 4 == n % 4 == 3:
				z = -1 * jacobi( n, a )
			else:
				z = jacobi( n, a )
		#i have tried to design the algorithm so any case will
		#be handled by the conditions above and this clause will not be reached
		else:
			z = 'fail'
			print z
		return z

	

#finds a primitive root for prime p
#this function was implemented from the algorithm described here:
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root( p ):
	if p == 2:
		return 1
	#the prime divisors of p-1 are 2 and (p-1)/2 because
	#p = 2x + 1 where x is a prime
	p1 = 2
	p2 = (p-1) / p1
	
	#test random g's until one is found that is a primitive root mod p
	while( 1 ):
		g = random.randint( 2, p-1 )
		if not modexp( g, (p-1)/p1, p ) == 1:
			if not modexp( g, (p-1)/p2, p ) == 1:
				return g

#find n bit prime
def find_prime():
	#keep testing until one is found
	while(1):
		#generate potential prime randomly
		p = random.randint( 2**(n-1), 2**n )
		#make sure it is odd
		while( p % 2 == 0 ):
			p = random.randint(2**(n-1),2**n)

		#keep doing this if the solovay-strassen test fails
		while( not SS(p) ):
			p = random.randint( 2**(n-1), 2**n )
			while( p % 2 == 0 ):
				p = random.randint(2**(n-1), 2**n)

		#if p is prime compute p = 2*p + 1
		#if p is prime, we have succeeded; else, start over
		p = p * 2 + 1
		if SS(p):
			return p
	
#encodes bytes to integers mod p.  reads bytes from file
def encode( file_name ):
	f = open( file_name, 'r' )
	data = ord(f.read(1))
	byte_array = []
	#put data into an array.  each element is a byte
	while( data ):
		byte_array.append( data )
		data = f.read(1)
		if data == '':
			break
		data = ord(data)
			
	f.close()

	#z is the array of integers mod 504
	z = []	#[0]*int(math.ceil( len(m) / (n/8) ))
	j = -(n/8)
	num = 0
	for i in range( len(byte_array) ):
		if i % (n/8) == 0:
			j += (n/8)
			num = 0
			z.append(0)
		z[j/(n/8)] += byte_array[i]*(2**(8*(i%(n/8))))


	return z

def decode():
	#get encoded integers from file
	f = open( 'Plaintext', 'r' )
	data = f.readline()
	z = []
	while( data ):
		if not data == '':
			data = int(data)
			print data
			z.append(data)
		data = f.readline
	f.close()

	#decode
	bytes_array = []
	for j in z:
		for i in range(n/8):
			if not j == (n/8)-1:
				bytes_array.append( j % (2**(8*i)) )
				j = j / ( 2**(8*i))
			else:
				bytes_array.append( j )

	f = open( 'Plaintext', 'w' )
	for i in bytes_array:
		print (chr(i))
		f.write( chr(i) )
	f.close()
				

	
def generate_keys():
	p = find_prime()
	g = find_primitive_root( p )
	x = random.randint( 1, p )
	h = modexp( g, x, p )

	keys = [[p, g, h], [p, g, x]]
	return keys

def get_global_params():
	global n
	n = int( raw_input( "Enter a bit length n " ) )
	global t
	t = int (raw_input( "Enter a confidence level t " ) )

def encrypt( z ):
	#get p, g, h of K1
	f = open( 'K1', 'r' )
	p = int(f.readline())
	g = int(f.readline())
	h = int(f.readline())
	f.close()

	#encrypt
	cipher_pairs = []
	for i in z:
		y = random.randint( 0, p )
		c = modexp( g, y, p )
		d = i*modexp( h, y, p) % p
		cipher_pairs.append( [c, d] )

	#write to file 'Cipher'
	f = open( 'Cipher', 'w' )
	for i in cipher_pairs:
		f.write( str(i[0]) + ' ' + str(i[1]) + '\n' )
	f.close()	

def decrypt( ):
	#get p, g, x of K2
	f = open( 'K2', 'r' )
	p = int(f.readline())
	g = int(f.readline())
	x = int(f.readline())
	f.close()

	#decrpyt
	f = open('Cipher', 'r')
	pair = f.readline()
	plaintext = []
	while( not pair == '' ):
		pair = pair.split( ' ' )
		c = int(pair[0])
		d = int(pair[1])
		s = modexp( c, x, p )
		plain = d*modexp( s, -1, p) % p
		plaintext.append( plain )
		pair = f.readline()
		
	f.close()
	f = open( 'Plaintext', 'w' )
	for i in plaintext:
		f.write( str(i) + "\n" )
	
if False:
	get_global_params()
	print "finding prime"
	print find_prime()
	print "generating keys"
	keys = generate_keys()
	f = open( 'K1', 'w' )
	for i in keys[0]:
		f.write( str(i) + "\n" )
	f.close
	f = open( 'K2', 'w' )
	for i in keys[1]:
		f.write( str(i) + "\n" )
	f.close()
	z = encode( 'message' )
	for i in z:
		print( "z[" + str(i) + "]=" + str(i) )
	print "encrypting"
	encrypt( z )
	print "decrypting"
	decrypt()
	print( 'done' )


get_global_params()
z = encode( 'message' )
f = open( 'Plaintext', 'w' )
for i in z:
	f.write( str(i) + "\n" )







