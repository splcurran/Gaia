# -*- coding: utf-8 -*-

import sys
import re
import math
import datetime
import time
import functools
import itertools
import random

import utilities

"""
OPERATORS

Here the operators are defined. Each operator is a function that accepts the stack
as an argument and modifies it in place.

"""

class Operator(object):

	def __init__(self, name, arity, func):
		self.name = name
		self.arity = arity
		self.func = func

	def execute(self, stack):
		if self.arity == 0:
			self.func(stack)
		elif self.arity == 1:
			if len(stack) > 0:
				z = stack.pop()
			else:
				z = utilities.getInput()
			mode = {int: 1, float: 1, str: 2, list: 3}[type(z)]
			self.func(stack, z, mode)
		elif self.arity == 2:
			if len(stack) >= 2:
				y = stack.pop()
				x = stack.pop()
			elif len(stack) == 1:
				x = stack.pop()
				y = utilities.getInput()
			else:
				x = utilities.getInput()
				y = utilities.getInput()
			self.func(stack, x, y, dyadMode(x,y))



""" HELPER FUNCTIONS """

def dyadMode(x, y):
	# Returns the mode the dyad should execute, based on the types of its arguments
	tx = type(x)
	ty = type(y)
	if tx == int or tx == float:
		if ty == int or ty == float:
			return 1
		elif ty == str:
			return 2
		elif ty == list:
			return 3
	elif tx == str:
		if ty == int or ty == float:
			return 4
		elif ty == str:
			return 5
		elif ty == list:
			return 6
	elif tx == list:
		if ty == int or ty == float:
			return 7
		elif ty == str:
			return 8
		elif ty == list:
			return 9
	else:
		return 0


def monadNotImplemented(mode, char):
	raise NotImplementedError('('+["num", "str", "list"][mode-1]+") "+char+" not implemented")

def dyadNotImplemented(mode, char):
	raise NotImplementedError('('+["num", "str", "list"][(mode-1)//3]+", "+["num", "str", "list"][mode%3-1]+") "+char+" not implemented")


# Increments an alphabetic string to the next string, alphabetically
def incrementWord(word):
	if len(word) == 0:
		return 'a'
	else:
		if word[-1] == 'z':
			if len(word) == 1:
				return 'aa'
			else:
				return incrementWord(word[:-1])+'a'
		elif word[-1] == 'Z':
			if len(word) == 1:
				return 'AA'
			else:
				return incrementWord(word[:-1])+'A'
		else:
			return word[:-1]+chr(ord(word[-1])+1)


""" OPERATOR FUNCTIONS """

''' NILADS '''

# ø
def emptySetOperator(stack):
	stack.append([])

# Ø
def emptyStringOperator(stack):
	stack.append("")

# ¶
def pilcrowOperator(stack):
	stack.append('\n')

# §
def sectionOperator(stack):
	stack.append(' ')

# @
def atOperator(stack):
	stack.append(utilities.getInput())

# €.
def extDotOperator(stack):
	print('STACK: '+utilities.outputFormat(stack))

# ₵a
def constaOperator(stack):
	stack.append('abcdefghijklmnopqrstuvwxyz')

# ₵A
def constAOperator(stack):
	stack.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# ₵v
def constvOperator(stack):
	stack.append('aeiou')

# ₵V
def constVOperator(stack):
	stack.append('AEIOU')

# ₵x
def constxOperator(stack):
	stack.append('bcdfghjklmnpqrstvwxz')

# ₵X
def constXOperator(stack):
	stack.append('BCDFGHJKLMNPQRSTVWXZ')

# ₵c
def constcOperator(stack):
	stack.append('bcdfghjklmnpqrstvwxyz')

# ₵C
def constCOperator(stack):
	stack.append('BCDFGHJKLMNPQRSTVWXYZ')

# ₵y
def constyOperator(stack):
	stack.append('aeiouy')

# ₵Y
def constYOperator(stack):
	stack.append('AEIOUY')

# ₵D
def constDOperator(stack):
	stack.append('0123456789')

# ₵H
def constHOperator(stack):
	stack.append('0123456789ABCDEF')

# ₵h
def consthOperator(stack):
	stack.append('0123456789abcdef')

# ₵q
def constqOperator(stack):
	stack.append(['qwertyuiop', 'asdfghjkl', 'zxcvbnm'])

# ₵Q
def constQOperator(stack):
	stack.append(['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'])

# ₵R
def constROperator(stack):
	stack.append(""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~""")

# ₵r
def constrOperator(stack):
	stack.append(utilities.codepage)

# ₵W
def constWOperator(stack):
	stack.append("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")

# ₸
def struckTOperator(stack):
	stack.append(10)

# ℍ
def struckHOperator(stack):
	stack.append(100)

# ₵P
def constPOperator(stack):
	stack.append(math.pi)

# ₵E
def constEOperator(stack):
	stack.append(math.e)

# ∂a
def dateaOperator(stack):
	stack.append(1 if datetime.datetime.today().hour >= 12 else 0)

# ∂A
def dateAOperator(stack):
	stack.append("PM" if datetime.datetime.today().hour >= 12 else "AM")

# ∂d
def datedOperator(stack):
	stack.append(datetime.datetime.today().day)

# ∂D
def dateDOperator(stack):
	stack.append("{:0>2}".format(datetime.datetime.today().day))

# ∂h
def datehOperator(stack):
	stack.append(datetime.datetime.today().hour)

# ∂H
def dateHOperator(stack):
	stack.append("{:0>2}".format(datetime.datetime.today().hour))

# ∂i
def dateiOperator(stack):
	stack.append(datetime.datetime.today().hour%12 or 12)

# ∂I
def dateIOperator(stack):
	stack.append("{:0>2}".format(datetime.datetime.today().hour%12 or 12))

# ∂k
def datekOperator(stack):
	stack.append([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# ∂K
def dateKOperator(stack):
	stack.append([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# ∂l
def datelOperator(stack):
	year = datetime.datetime.today().year
	stack.append(1 if ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0) else 0)

# ∂L
def dateLOperator(stack):
	year = datetime.datetime.today().year
	while not ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
		year += 1
	stack.append(year)

# ∂m
def datemOperator(stack):
	stack.append(datetime.datetime.today().month)

# ∂M
def dateMOperator(stack):
	stack.append("{:0>2}".format(datetime.datetime.today().month))

# ∂n
def datenOperator(stack):
	stack.append(datetime.datetime.today().minute)

# ∂N
def dateNOperator(stack):
	stack.append("{:0>2}".format(datetime.datetime.today().minute))

# ∂o
def dateoOperator(stack):
	stack.append(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

# ∂O
def dateOOperator(stack):
	stack.append(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

# ∂q
def dateqOperator(stack):
	stack.append(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

# ∂Q
def dateQOperator(stack):
	stack.append(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

# ∂t
def datetOperator(stack):
	stack.append([datetime.datetime.today().hour, datetime.datetime.today().minute, datetime.datetime.today().second])

# ∂T
def dateTOperator(stack):
	stack.append([datetime.datetime.today().hour%12 or 12, datetime.datetime.today().minute, datetime.datetime.today().second, 1 if datetime.datetime.today().hour >= 12 else 0])

# ∂s
def datesOperator(stack):
	stack.append(datetime.datetime.today().second)

# ∂S
def dateSOperator(stack):
	stack.append("{:0>2}".format(datetime.datetime.today().second))

# ∂u
def dateuOperator(stack):
	stack.append(datetime.datetime.today().microsecond//1000)

# ∂U
def dateUOperator(stack):
	stack.append(datetime.datetime.today().microsecond)

# ∂w
def datewOperator(stack):
	stack.append(datetime.datetime.today().isoweekday()%7+1)

# ∂W
def dateWOperator(stack):
	stack.append(datetime.datetime.today().isoweekday())

# ∂x
def datexOperator(stack):
	stack.append([datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day])

# ∂X
def dateXOperator(stack):
	d = datetime.datetime.today()
	stack.append([d.year, d.month, d.today().day, d.isoweekday()%7+1, d.hour, d.minute, d.second, d.microsecond//1000])

# ∂y
def dateyOperator(stack):
	stack.append(datetime.datetime.today().year)

# ∂Y
def dateYOperator(stack):
	stack.append(datetime.datetime.today().year%100)

# ∂z
def datezOperator(stack):
	stack.append(time.timezone//-3600)

# ∂Z
def dateZOperator(stack):
	stack.append(int(time.time()*1000))

''' MONADS '''

# !
def exclamationOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(1 if not z else 0)
	else:
		monadNotImplemented(mode, '')

# $
def dollarOperator(stack, z, mode):
	if mode == 1:   # num
		result = []
		sign = -1 if z<0 else 1
		z = abs(z)
		while z != 0:
			result.insert(0, (z % 10)*sign)
			z //= 10
		stack.append(result)
	elif mode == 2: # str
		stack.append(list(z))
	elif mode == 3: # list
		stack.append(''.join(utilities.castToString(i) for i in z))
	else:
		monadNotImplemented(mode, '')

# (
def leftParenthesisOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(z-1))
	elif mode == 2: # str
		if len(z) > 0:
			stack.append(z[0])
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[0])
	else:
		monadNotImplemented(mode, '')

# )
def rightParenthesisOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(z+1))
	elif mode == 2: # str
		if len(z) > 0:
			stack.append(z[-1])
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[-1])
	else:
		monadNotImplemented(mode, '')

# :
def colonOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(z)
		stack.append(z)
	else:
		monadNotImplemented(mode, '')

# b
def bOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.toBase(int(z), 2))
	#elif mode == 2: # str
	elif mode == 3: # list
		stack.append(utilities.fromBase([utilities.castToNumber(i) for i in z], 2))
	else:
		monadNotImplemented(mode, '')

# c
def cOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(chr(int(z)))
	elif mode == 2: # str
		if z:
			stack.append(ord(z[0]))
	elif mode == 3: # list
		z = [utilities.castToNumber(i) for i in z]
		stack.append(utilities.fromBase(z, max(z)+1))
	else:
		monadNotImplemented(mode, '')

# d
def dOperator(stack, z, mode):
	if mode == 1:   # num
		z = abs(int(z))
		stack.append([i for i in range(1, z+1) if z%i==0])
	elif mode == 2: # str
		stack.append(utilities.castToNumber(z))
	elif mode == 3: # list
		stack.append(utilities.castToNumber(z))
	else:
		monadNotImplemented(mode, '')

# e is defined in gaia.py

# f
def fOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(math.factorial(int(z)))
	elif mode == 2: # str
		stack.append([''.join(p) for p in itertools.permutations(z)])
	elif mode == 3: # list
		stack.append([list(p) for p in itertools.permutations(z)])
	else:
		monadNotImplemented(mode, '')

# g
def gOperator(stack, z, mode):
	if mode == 1:   # num
		1#stack.append()
	elif mode == 2: # str
		args = sys.argv
		args = args[1:]
		if len(args) > 0:
			if re.match('^-', args[0]):
				# If the next arg starts with - it has flags
				flags = list(args[0][1:])
				args = args[1:]

		filepath = args[0]
		filepath = re.sub('(/|^)[^/]*$','\g<1>',filepath) # Get the filepath for where the source is
		if z == '':
			z = args[0] # If z is empty then use the source file
		else:
			z = filepath + z

		stack.append(open(z, 'r', encoding='utf-8').read())
	elif mode == 3: # list
		gradeup = lambda l:[x[1]+1 for x in sorted([[l[i], i] for i in range(len(l))])]
		stack.append(gradeup(z))
	else:
		monadNotImplemented(mode, '')

# h
def hOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.toBase(int(z), 16))
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		stack.append(utilities.fromBase(z, 16))
	else:
		monadNotImplemented(mode, '')

# i
def iOperator(stack, z, mode):
	if mode > 0:
		stack.append(z)
	else:
		monadNotImplemented(mode, '')

# l
def lOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(len(str(z)))
	elif mode == 2: # str
		stack.append(len(z))
	elif mode == 3: # list
		stack.append(len(z))
	else:
		monadNotImplemented(mode, '')

# n
def nOperator(stack, z, mode):
	#if mode == 1:   # num
	#elif mode == 2: # str
	if mode == 3: # list
		def depth(l):
			if type(l) != list:
				return 0
			d = 1
			for i in l:
				if type(l) == list:
					d = max(d, 1+depth(i))
			return d
		stack.append(depth(z))
	else:
		monadNotImplemented(mode, '')

# o
def oOperator(stack, z, mode):
	if mode == 2: # str
		stack.append(1 if sorted(z) in [z, z[::-1]] else 0)
	elif mode == 3: # list
		stack.append(1 if sorted(z) in [z, z[::-1]] else 0)
	else:
		monadNotImplemented(mode, '')

# p
def pOperator(stack, z, mode):
	if mode > 0:   # any types
		sys.stdout.write(utilities.outputFormat(z))
		utilities.manualOutput = True
	else:
		monadNotImplemented(mode, '')

# q
def qOperator(stack, z, mode):
	if mode > 0:   # any types
		print(utilities.outputFormat(z))
		utilities.manualOutput = True
	else:
		monadNotImplemented(mode, '')

# r
def rOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(int(z)%2)
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		result = []
		for i in range(len(z)):
			for j in range(len(z)):
				if i != j and [z[j], z[i]] not in result:
					result.append([z[i], z[j]])
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

# s
def sOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(z*z))
	elif mode == 2: # str
		stack.append([[i, z[i-1]] for i in range(1,len(z)+1)])
	elif mode == 3: # list
		stack.append([[i, z[i-1]] for i in range(1,len(z)+1)])
	else:
		monadNotImplemented(mode, '')

# t
def tOperator(stack, z, mode):
	if mode == 1:   # num
		n = int(z)
		p = 0
		factors = []
		while n > 1:
			count = 0
			while n%utilities.getPrime(p) == 0:
				n //= utilities.getPrime(p)
				count += 1
			if count > 0:
				factors.append(utilities.getPrime(p))
			p += 1
		for f in factors:
			z *= (f-1)/f
		stack.append(utilities.formatNum(z))
	#elif mode == 2: # str
	elif mode == 3: # list
		z = [i if type(i)==list else [i] for i in z]

		maxrow = max(map(len, z))
		newmatrix = []

		for c in range(maxrow):
			newrow = []
			for r in z:
				if len(r) > c:
					newrow.append(r[c])
			newmatrix.append(newrow)
		stack.append(newmatrix)
	else:
		monadNotImplemented(mode, 't')

# u
def uOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.sqrt(z)))
	elif mode == 2: # str
		stack.append(''.join([z[i] for i in range(len(z)) if z[i] not in z[:i]]))
	elif mode == 3: # list
		stack.append([z[i] for i in range(len(z)) if z[i] not in z[:i]])
	else:
		monadNotImplemented(mode, '')

# v
def vOperator(stack, z, mode):
	if mode == 1:   # num
		sign = -1 if z < 0 else 1
		z = abs(z)
		stack.append(sign*utilities.formatNum(float(str(z)[::-1])))
	elif mode == 2: # str
		stack.append(z[::-1])
	elif mode == 3: # list
		stack.append(z[::-1])
	else:
		monadNotImplemented(mode, '')

# w
def wOperator(stack, z, mode):
	if mode > 0: # any types
		stack.append([z])
	else:
		monadNotImplemented(mode, '')

# y
def yOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(1 if int(z)==z else 0)
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		if z:
			stack.append(1 if all(i == z[0] for i in z) else 0)
		else:
			stack.append(1)
	else:
		monadNotImplemented(mode, '')

# \
def backslashOperator(stack, z , mode):
	if mode == 0:
		monadNotImplemented(mode, '')

# _
def underscoreOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(-z))
	#elif mode == 2: # str
	elif mode == 3: # list
		stack.append(utilities.flatten(z))
	else:
		monadNotImplemented(mode, '')

# ~
def tildeOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(~int(z))
	elif mode == 2: # str
		stack.append(''.join([c.upper() if c.islower() else (c.lower() if c.isupper() else c) for c in z]))
	elif mode == 3: # list
		stack.append()
	else:
		monadNotImplemented(mode, '')

# …
def lowEllipsisOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		if z == 0:
			stack.append([])
		elif z > 0:
			stack.append(list(range(z)))
		elif z < 0:
			stack.append(list(range(0, z, -1)))
	elif mode == 2: # str
		stack.append([z[:i+1] for i in range(len(z))])
	elif mode == 3: # list
		stack.append([z[:i+1] for i in range(len(z))])
	else:
		monadNotImplemented(mode, '')

# ┅
def highEllipsisOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		if z == 0:
			stack.append([0])
		elif z > 0:
			stack.append(list(range(1, z+1)))
		elif z < 0:
			stack.append(list(range(-1, z-1, -1)))
	elif mode == 2: # str
		stack.append([z[-len(z)+i:] for i in range(len(z))])
	elif mode == 3: # list
		stack.append([z[-len(z)+i:] for i in range(len(z))])
	else:
		monadNotImplemented(mode, '')

# ⌋
def floorOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(int(math.floor(z)))
	elif mode == 2: # str
		stack.append(z.lower())
	elif mode == 3: # list
		#z = [utilities.castToNumber(i) for i in z]
		if z == []:
			stack.append(0)
		else:
			stack.append(min(z))
	else:
		monadNotImplemented(mode, '')

# ⌉
def ceilOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(int(math.ceil(z)))
	elif mode == 2: # str
		stack.append(z.upper())
	elif mode == 3: # list
		#z = [utilities.castToNumber(i) for i in z]
		if z == []:
			stack.append(0)
		else:
			stack.append(max(z))
	else:
		monadNotImplemented(mode, '')

# Σ
def sigmaOperator(stack, z, mode):
	if mode == 1:   # num
		tempStack = []
		dollarOperator(tempStack, z, mode)
		stack.append(sum(tempStack[0]))
	#elif mode == 2: # str
	elif mode == 3: # list
		stack.append(sum(utilities.castToNumber(i) for i in z))
	else:
		monadNotImplemented(mode, '')

# Π
def piOperator(stack, z, mode):
	if mode == 1:   # num
		tempStack = []
		dollarOperator(tempStack, z, mode)
		stack.append(functools.reduce(lambda a,b:a*b, tempStack[0]))
	#elif mode == 2: # str
	elif mode == 3: # list
		if z == []:
			stack.append(1)
		else:
			stack.append(functools.reduce(lambda a,b:a*b, [utilities.castToNumber(i) for i in utilities.flatten(z)]))
	else:
		monadNotImplemented(mode, '')

# ‼
def doubleExclamationOperator(stack, z, mode):
	if mode > 0:   # Any types
		stack.append(1 if z else 0)
	else:
		monadNotImplemented(mode, '')

# ċ
def cHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append([0]*abs(int(z)))
	elif mode == 2: # str
		stack.append([ord(i) for i in z])
	elif mode == 3: # list
		stack.append(list(range(1,len(z)+1)))
	else:
		monadNotImplemented(mode, '')

# 
def dHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		if z < 4:
			stack.append([z, 1])
		else:
			p = 0
			result = []
			while z > 1:
				count = 0
				while z%utilities.getPrime(p) == 0:
					z //= utilities.getPrime(p)
					count += 1
				if count > 0:
					result.append([utilities.getPrime(p), count])
				p += 1
			stack.append(result)
	elif mode == 2 or mode == 3: # str or list
		if len(z)==0:
			stack.append([])
		result = []
		for i in range(len(z)):
			for j in range(len(z), 0, -1):
				if i < j:
					result.append(z[i:j])
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

# ḍ
def dLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		if z < 4:
			stack.append([z])
		else:
			p = 0
			result = []
			while z > 1:
				while z%utilities.getPrime(p) == 0:
					result.append(utilities.getPrime(p))
					z //= utilities.getPrime(p)
				p += 1
			stack.append(result)
	elif mode == 2 or mode == 3: # str or list
		def partitions(z):
			if len(z) == 0:
				return [[]]
			if len(z) == 1:
				return [[z]]
			return [[z[:i]]+t for i in range(1, len(z)+1) for t in partitions(z[i:])]
		stack.append(partitions(z))
	else:
		monadNotImplemented(mode, '')

# ė
def eHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.cos(z)))
	elif mode == 2 or mode == 3: # str or list
		if len(z) == 0:
			stack.append([])
		else:
			current = None
			count = 0
			result = []
			for i in z:
				if current != i:
					if current != None:
						result.append([count, current])
					current = i
					count = 1
				else:
					count += 1
			stack.append(result)
	else:
		monadNotImplemented(mode, '')

# ẹ
def eLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.acos(z)))
	#elif mode == 2:
	elif mode == 3: # str or list
		if len(z) == 0:
			stack.append([])
		else:
			result = ""
			for i in z:
				i = utilities.castToList(i)
				if len(i) >= 2:
					if type(i[1]) == str and type(result) == str:
						result += (i[1] * utilities.castToNumber(i[0]))
					else:
						result = list(result)
						result += [i[1]] * utilities.castToNumber(i[0])
			stack.append(result)
	else:
		monadNotImplemented(mode, '')

# ḟ
def fHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		def subfactorial(n):
			soFar = [1, 0]
			if n < 0:
				raise ValueError("can't comput subfactorial of negative number")
			if n < 2:
				return soFar[n]

			i = 2
			while i <= n:
				soFar.append((i-1)*(soFar[i-1]+soFar[i-2]))
				i += 1

			return soFar[-1]

		stack.append(subfactorial(int(z)))
	elif mode == 2: # str
		stack.append([''.join(p) for p in itertools.permutations(z) if all(''.join(p)[i] != z[i] for i in range(len(z)))])
	elif mode == 3: # list
		stack.append([list(p) for p in itertools.permutations(z) if all(list(p)[i] != z[i] for i in range(len(z)))])
	else:
		monadNotImplemented(mode, '')

# ḣ
def hHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(z*2))
	elif mode == 2: # str
		stack.append(z[:-1] if z else "")
	elif mode == 3: # list
		stack.append(z[:-1] if z else [])
	else:
		monadNotImplemented(mode, '')

# ḥ
def hLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(z/2))
	elif mode == 2: # str
		stack.append(z[1:] if z else "")
	elif mode == 3: # list
		stack.append(z[1:] if z else [])
	else:
		monadNotImplemented(mode, '')

# ṁ
def mHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		stack.append(stack.pop(len(stack)-((z-1)%len(stack))-1))
	#elif mode == 2: # str
	elif mode == 3: # list
		if z==[]:
			stack.append([])
		else:
			m = max(z)
			stack.append([i for i in z if i==m])
	else:
		monadNotImplemented(mode, '')

# ṃ
def mLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		stack.append(stack[len(stack)-((z-1)%len(stack))-1])
	#elif mode == 2: # str
	elif mode == 3: # list
		if z==[]:
			stack.append([])
		else:
			m = min(z)
			stack.append([i for i in z if i==m])
	else:
		monadNotImplemented(mode, '')

# ṅ
def nHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		if (z > 0):
			stack.append(utilities.getPrimes(int(z)))
		else:
			stack.append([])
	elif mode == 2: # str
		if len(z) > 0:
			stack.append(z[:-1])
			stack.append(z[-1])
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[:-1])
			stack.append(z[-1])
	else:
		monadNotImplemented(mode, '')

# ṇ
def nLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		if (z > 0):
			stack.append(utilities.getPrime(int(z)))
	elif mode == 2: # str
		if len(z) > 0:
			stack.append(z[1:])
			stack.append(z[0])
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[1:])
			stack.append(z[0])
	else:
		monadNotImplemented(mode, '')

# ȯ
def oHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(abs(z))
	elif mode == 2: # str
		stack.append(''.join(sorted(z)))
	elif mode == 3: # list
		stack.append(sorted(z))
	else:
		monadNotImplemented(mode, '')

# ọ
def oLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(-1 if z < 0 else (1 if z > 0 else 0))
	elif mode == 2: # str
		stack.append(z.strip())
	elif mode == 3: # list
		if len(z) <= 1:
			stack.append([])
		else:
			stack.append([z[i+1]-z[i] for i in range(len(z)-1)])
	else:
		monadNotImplemented(mode, '')

# ṗ
def pHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		if z < 2:
			stack.append(0)
		else:
			while utilities.getPrime(-1) < z:
				utilities.generatePrime()
			stack.append(1 if z in utilities.getPrimes(-1) else 0)
	#elif mode == 2: # str
	#elif mode == 3: # list
	else:
		monadNotImplemented(mode, '')

# ṙ
def rHighDotOperator(stack, z, mode):
	# TODO this isn't quite right because of the weird issue with the quote characters
	if mode == 1:   # num
		stack.append(str(z))
	elif mode == 2: # str
		stack.append('“'+re.sub('[\\\\“”‘’„‟]', '\\\\\g<0>', z)+'”') # TODO this should be used for the output format...
	elif mode == 3: # list
		stack.append(utilities.outputFormat(z))
	else:
		monadNotImplemented(mode, '')

# ṛ
def rLowDotOperator(stack, z, mode):
	random.seed()
	if mode == 1:   # num
		stack.append(random.randint(1, int(z)+1))
	elif mode == 2: # str
		stack.append(random.choice(z))
	elif mode == 3: # list
		stack.append(random.choice(z))
	else:
		monadNotImplemented(mode, '')

# ṡ
def sHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.sin(z)))
	elif mode == 2: # str
		stack.append(z.split(' '))
	elif mode == 3: # list
		stack.append(' '.join(map(utilities.castToString, z)))
	else:
		monadNotImplemented(mode, '')

# ṣ
def sLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.asin(z)))
	elif mode == 2: # str
		stack.append(z.split('\n'))
	elif mode == 3: # list
		stack.append('\n'.join(map(utilities.castToString, z)))
	else:
		monadNotImplemented(mode, '')

# ṫ
def tHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.tan(z)))
	elif mode == 2: # str
		if z == "":
			stack.append("")
		else:
			stack.append(z + z[-2::-1])
	elif mode == 3: # list
		if z == []:
			stack.append([])
		else:
			stack.append(z + z[-2::-1])
	else:
		monadNotImplemented(mode, '')

# ṭ
def tLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(math.atan(z)))
	elif mode == 2 or mode == 3: # str or list
		stack.append(1 if z[::-1]==z else 0)
	else:
		monadNotImplemented(mode, '')

# ụ
def uLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		if z >= 0:
			stack.append(1 if int(math.sqrt(z)) == math.sqrt(z) else 0)
		else:
			stack.append(0)
	elif mode == 2: # str
		stack.append([s.split() for s in z.split('\n')])
	elif mode == 3: # list
		stack.append('\n'.join(' '.join(utilities.castToString(w) for w in s) if type(s)==list else utilities.castToString(s) for s in z))
	else:
		monadNotImplemented(mode, '')

# ẋ
def xHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(1/z))
	elif mode == 2: # str
		result = []

		currentRun = None
		start = 0
		for i in range(len(z)):
			if currentRun == None:
				currentRun = z[i]
			if z[i] != currentRun:
				currentRun = z[i]
				result.append(z[start:i])
				start = i
		result.append(z[start:])
		stack.append(result)
	elif mode == 3: # list
		result = []

		currentRun = None
		start = 0
		for i in range(len(z)):
			if currentRun == None:
				currentRun = z[i]
			if z[i] != currentRun:
				currentRun = z[i]
				result.append(z[start:i])
				start = i
		result.append(z[start:])
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

# ẏ
def yHighDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(1 if z > 0 else 0)
	elif mode == 2: # str
		stack.append(1 if all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in z) else 0)
	elif mode == 3: # list
		stack.append(1 if all(z) else 0)
	else:
		monadNotImplemented(mode, '')

# ỵ
def yLowDotOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(1 if z < 0 else 0)
	elif mode == 2: # str
		stack.append(1 if all(c in 'abcdefghijklmnopqrstuvwxyz' for c in z) else 0)
	elif mode == 3: # list
		stack.append(1 if all(not i for i in z) else 0)
	else:
		monadNotImplemented(mode, '')

# z
def zOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(2**z))
	#elif mode == 2: # str
	elif mode == 3: # list
		p=lambda s:[s[:1]+t for t in p(s[1:])]+p(s[1:])if s else [s]
		stack.append(p(z))
	else:
		monadNotImplemented(mode, '')

#-- Extended Monads -- #

# €[
def extLeftBracketOperator(stack, z, mode):
	if mode == 1:   # num
		1#stack.append()
	#elif mode == 2: # str
	elif mode == 3: # list
		z = [re.sub("^\s*([\s\S]*?)\s*$", "\g<1>", utilities.castToString(i)) for i in z]
		maxLength = max(len(i) for i in z)

		result = [i+(maxLength-len(i))*' ' for i in z]
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

# €|
def extPipeOperator(stack, z, mode):
	if mode == 1:   # num
		1#stack.append()
	#elif mode == 2: # str
	elif mode == 3: # list
		z = [re.sub("^\s*([\s\S]*?)\s*$", "\g<1>", utilities.castToString(i)) for i in z]
		maxLength = max(len(i) for i in z)

		result = [(math.ceil((maxLength-len(i))/2)*' ')+i+(math.floor((maxLength-len(i))/2)*' ') for i in z]
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

# €]
def extRightBracketOperator(stack, z, mode):
	if mode == 1:   # num
		1#stack.append()
	#elif mode == 2: # str
	elif mode == 3: # list
		z = [re.sub("^\s*([\s\S]*?)\s*$", "\g<1>", utilities.castToString(i)) for i in z]
		maxLength = max(len(i) for i in z)

		result = [(maxLength-len(i))*' '+i for i in z]
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

''' DYADS '''

# %
def percentOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x % y))
	elif mode == 2: # num, str
		stack.append(y[::int(x)])
	elif mode == 3: # num, list
		stack.append(y[::int(x)])
	elif mode == 4: # str, num
		stack.append(x[::int(y)])
	elif mode == 5: # str, str
		s = x.split(y)
		result = []
		for i in s[:-1]:
			result += [i, y]
		result .append(s[-1])
		stack.append(result)
	elif mode == 6 or mode == 8: # str, list; list, str
		s = x if mode == 6 else y
		l = y if mode == 6 else x

		result = []
		start = 0

		for i in range(len(l)):
			if l[i] == s:
				result.append(l[start:i])
				result.append([s])
				start = i+1
		result.append(l[start:])

		stack.append(result)
	elif mode == 7: # list, num
		stack.append(x[::int(y)])
	elif mode == 9: # list, list
		result = []
		i=0
		while i<len(x):
			if x[i:i+len(y)] == y:
				result.append(x[:i])
				result.append(y)
				x = x[i+len(y):]
				i = 0
			else:
				i += 1

		result.append(x)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# &
def ampersandOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) & int(y))
	elif mode == 2 or mode == 4 or mode == 3 or mode == 7: # num, str; str, num; num, list; lsit, num
		(s,n) = (x,y) if mode == 4 or mode == 7 else (y,x)

		result = "" if mode == 2 or mode == 4 else []

		for i in s:
			result += (i if mode == 2 or mode == 4 else [i])*abs(n)

		stack.append(result[::-1 if n<0 else 1])
	elif mode == 5: # str, str
		result = ""
		for c in x:
			if c in y and c not in result:
				result += c
		stack.append(result)
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		result = []
		for i in x:
			if i in y and i not in result:
				result.append(i)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# *
def asteriskOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x ** y))
	#elif mode == 2: # num, str
	elif mode == 3 or mode == 7: # num, list; list, num
		n = x if mode == 3 else y
		l = y if mode == 3 else x

		if n == 0:
			stack.append([])
			return
		elif n < 0:
			raise ValueError("can't do Cartesian power with negative exponent")

		start = [[i] for i in l]
		result = start
		for i in range(int(n)-1):
			result = [i+j for i in result for j in start]

		stack.append(result)
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		stack.append(''.join(i for i in x if i in y))
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append([i for i in x if i in y])
	else:
		dyadNotImplemented(mode, '')

# +
def plusOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x + y))
	elif mode == 2: # num, str
		stack.append(str(x) + y)
	elif mode == 3: # num, list
		stack.append([x] + y)
	elif mode == 4: # str, num
		stack.append(x + str(y))
	elif mode == 5: # str, str
		stack.append(x + y)
	elif mode == 6: # str, list
		stack.append([x] + y)
	elif mode == 7: # list, num
		stack.append(x + [y])
	elif mode == 8: # list, str
		stack.append(x + [y])
	elif mode == 9: # list, list
		stack.append(x + y)
	else:
		dyadNotImplemented(mode, '+')

# ,
def commaOperator(stack, x, y, mode):
	if mode > 0: # any types
		stack.append([x, y])
	else:
		dyadNotImplemented(mode, '')

# /
def slashOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x // y))
	elif mode == 2: # num, str
		if x <= 0:
			raise ValueError("invalid size for splitting: "+str(int(x)))
		stack.append([y[i:i+int(x)] for i in range(0, len(y), int(x))])
	elif mode == 3: # num, list
		if x <= 0:
			raise ValueError("invalid size for splitting: "+str(int(x)))
		stack.append([y[i:i+int(x)] for i in range(0, len(y), int(x))])
	elif mode == 4: # str, num
		if y <= 0:
			raise ValueError("invalid size for splitting: "+str(int(y)))
		stack.append([x[i:i+int(y)] for i in range(0, len(x), int(y))])
	elif mode == 5: # str, str
		result = x.split(y)
		while "" in result:
			result.remove("")
		stack.append(result)
	elif mode == 6 or mode == 8: # str, list; list, str
		l = y if mode == 6 else x
		s = x if mode == 6 else y

		result = []
		i=0
		while i<len(l):
			if l[i] == s:
				if i > 0: # Don't append an empty list
					result.append(l[:i])
				l = l[i+1:]
				i = 0
			else:
				i += 1

		result.append(l)
		stack.append(result)

	elif mode == 7: # list, num
		if y <= 0:
			raise ValueError("invalid size for splitting: "+str(int(y)))
		stack.append([x[i:i+int(y)] for i in range(0, len(x), int(y))])
	elif mode == 9: # list, list
		result = []
		i=0
		while i<len(x):
			if x[i:i+len(y)] == y:
				if i > 0: # Don't append an empty list
					result.append(x[:i])
				x = x[i+len(y):]
				i = 0
			else:
				i += 1

		result.append(x)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# ;
def semicolonOperator(stack, x, y, mode):
	if mode > 0: # any types
		stack.append(x)
		stack.append(y)
		stack.append(x)
	else:
		dyadNotImplemented(mode, '')

# <
def lessThanOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x < y else 0)
	elif mode == 2: # num, str
		stack.append(y[:x])
	elif mode == 3: # num, list
		stack.append(y[:x])
	elif mode == 4: # str, num
		stack.append(x[:y])
	elif mode == 5: # str, str
		stack.append(1 if x < y else 0)
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		stack.append(x[:y])
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if x < y else 0)
	else:
		dyadNotImplemented(mode, '')

# =
def equalsOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x == y else 0)
	elif mode == 2: # num, str
		stack.append(y[(int(x)-1)%len(y)])
	elif mode == 3: # num, list
		stack.append(y[(int(x)-1)%len(y)])
	elif mode == 4: # str, num
		stack.append(x[(int(y)-1)%len(x)])
	elif mode == 5: # str, str
		stack.append(1 if x == y else 0)
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		stack.append(x[(int(y)-1)%len(x)])
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if x == y else 0)
	else:
		dyadNotImplemented(mode, '')

# >
def greaterThanOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x > y else 0)
	elif mode == 2: # num, str
		stack.append(y[x:])
	elif mode == 3: # num, list
		stack.append(y[x:])
	elif mode == 4: # str, num
		stack.append(x[y:])
	elif mode == 5: # str, str
		stack.append(1 if x > y else 0)
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		stack.append(x[y:])
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if x > y else 0)
	else:
		dyadNotImplemented(mode, '')

# ^
def caretOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) ^ int(y))
	#elif mode == 2: # num, str
	#elif mode == 3: # num, list
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		result = ""

		for c in x:
			if c not in y and c not in result:
				result += c

		for c in y:
			if c not in x and c not in result:
				result += c

		stack.append(result)
	#elif mode == 6: # str, list
	#elif mode == 7: # list, num
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		result = []

		for i in x:
			if i not in y and i not in result:
				result.append(i)

		for i in y:
			if i not in x and i not in result:
				result.append(i)

		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# |
def pipeOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) | int(y))
	#elif mode == 2: # num, str
	#elif mode == 3: # num, list
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		result = ""
		for c in x+y:
			if c not in result:
				result += c
		stack.append(result)
	#elif mode == 6: # str, list
	#elif mode == 7: # list, num
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		result = []
		for i in x+y:
			if i not in result:
				result.append(i)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# «
def leftArrowQuoteOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) << int(y))
	elif mode == 2: # num, str
		stack.append(y[int(x):]+y[:int(x)])
	elif mode == 3: # num, list
		stack.append(y[int(x):]+y[:int(x)])
	elif mode == 4: # str, num
		stack.append(x[int(y):]+x[:int(y)])
	elif mode == 5: # str, str
		stack.append(1 if (x[:len(y)] == y) else 0)
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		stack.append(x[int(y):]+x[:int(y)])
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if (x[:len(y)] == y) else 0)
	else:
		dyadNotImplemented(mode, '')

# »
def rightArrowQuoteOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) >> int(y))
	elif mode == 2: # num, str
		stack.append(y[-int(x):]+y[:-int(x)])
	elif mode == 3: # num, list
		stack.append(y[-int(x):]+y[:-int(x)])
	elif mode == 4: # str, num
		stack.append(x[-int(y):]+x[:-int(y)])
	elif mode == 5: # str, str
		stack.append(1 if (x[-len(y):] == y) else 0)
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		stack.append(x[-int(y):]+x[:-int(y)])
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if (x[-len(y):] == y) else 0)
	else:
		dyadNotImplemented(mode, '')

# ⊂
def subsetOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x <= y else 0)
	elif mode == 2 or mode == 4: # num, str; str, num
		s = y if mode == 2 else x
		n = int(x if mode == 2 else y)

		char = s[0] if len(s)>0 else ' '
		while len(s) < n:
			s = char+s

		stack.append(s)
	elif mode == 3 or mode == 7: # num, list
		l = y if mode == 3 else x
		n = int(x if mode == 3 else y)

		ele = l[0] if len(l)>0 else 0
		while len(l) < n:
			l = [ele]+l

		stack.append(l)
	elif mode == 5: # str, str
		stack.append(1 if all(i in y for i in x) else 0)
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if all(i in y for i in x) else 0)
	else:
		dyadNotImplemented(mode, '')

# ⊃
def supersetOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x >= y else 0)
	elif mode == 2 or mode == 4: # num, str; str, num
		s = y if mode == 2 else x
		n = int(x if mode == 2 else y)

		char = s[-1] if len(s)>0 else ' '
		while len(s) < n:
			s = s+char

		stack.append(s)
	elif mode == 3 or mode == 7: # num, list
		l = y if mode == 3 else x
		n = int(x if mode == 3 else y)

		ele = l[-1] if len(l)>0 else 0
		while len(l) < n:
			l = l+[ele]

		stack.append(l)
	elif mode == 5: # str, str
		stack.append(1 if all(i in x for i in y) else 0)
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(1 if all(i in x for i in y) else 0)
	else:
		dyadNotImplemented(mode, '')

# ∧
def andOperator(stack, x, y, mode):
	if mode > 0: # Same for any types...
		stack.append(x and y)
	else:
		dyadNotImplemented(mode, '')

# ∨
def orOperator(stack, x, y, mode):
	if mode > 0: # Same for any types...
		stack.append(x or y)
	else:
		dyadNotImplemented(mode, '')

# ×
def timesOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x * y))
	elif mode == 2: # num, str
		result = abs(int(x)) * y
		stack.append(result[::-1] if x < 0 else result)
	elif mode == 3: # num, list
		result = abs(int(x)) * y
		stack.append(result[::-1] if x < 0 else result)
	elif mode == 4: # str, num
		result = abs(int(y)) * x
		stack.append(result[::-1] if y < 0 else result)
	elif mode == 5: # str, str
		stack.append([i+j for i in x for j in y])
	elif mode == 6: # str, list
		stack.append(x.join(map(str, y)))
	elif mode == 7: # list, num
		result = abs(int(y)) * x
		stack.append(result[::-1] if y < 0 else result)
	elif mode == 8: # list, str
		stack.append(y.join(map(str, x))) # TODO this is weird when the list has sublists
	elif mode == 9: # list, list
		stack.append([[i, j] for i in x for j in y])
	else:
		dyadNotImplemented(mode, '×')

# ÷
def divisionOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x / y))
	elif mode == 2 or mode == 3 or mode == 4 or mode == 7: # num, str (2) or str, num (4) or num, list (3) or list, num (7)
		n = x if mode == 2 or mode == 3 else y
		s = y if mode == 2 or mode == 3 else x

		n = int(n) # Takes an integer specifically as argument
		if n > len(s) or n < 1:
			raise ValueError(str(n)+" is not a valid number of splits for "+utilities.outputFormat(s)+" (length "+str(len(s))+")")

		cuts = [0]*n
		result = []

		for i in range(len(s)):
			cuts[i%n] += 1

		for cut in cuts:
			result.append(s[:cut])
			s = s[cut:]

		stack.append(result)
	elif mode == 5: # str, str
		stack.append(x.split(y))
	elif mode == 6 or mode == 8: # str, list; list, str
		l = y if mode == 6 else x
		s = x if mode == 6 else y

		result = []
		i=0
		while i<len(l):
			if l[i] == s:
				result.append(l[:i])
				l = l[i+1:]
				i = 0
			else:
				i += 1

		result.append(l)
		stack.append(result)
	elif mode == 9: # list, list
		result = []
		i=0
		while i<len(x):
			if x[i:i+len(y)] == y:
				result.append(x[:i])
				x = x[i+len(y):]
				i = 0
			else:
				i += 1

		result.append(x)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# ⁻
def minusOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x - y))
	#elif mode == 2: # num, str
	elif mode == 3: # num, list
		stack.append([i for i in y if i != x])
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		stack.append(''.join(c for c in x if c not in y))
	elif mode == 6: # str, list
		stack.append([i for i in y if i != x])
	elif mode == 7: # list, num
		stack.append([i for i in x if i != y])
	elif mode == 8: # list, str
		stack.append([i for i in x if i != y])
	elif mode == 9: # list, list
		stack.append([i for i in x if i not in y])
	else:
		dyadNotImplemented(mode, '')

# B
def BOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.toBase(int(x), int(y)))
	elif mode == 2: # num, str
		stack.append(''.join(y[i] for i in utilities.toBase(int(x), len(y))))
	elif mode == 3: # num, list
		stack.append(utilities.fromBase(y, int(x)))
	elif mode == 4: # str, num
		stack.append(''.join(x[i] for i in utilities.toBase(int(y), len(x))))
	elif mode == 5: # str, str
		digitList = [y.find(c) if c in y else 0 for c in x]
		stack.append(utilities.fromBase(digitList, len(y)))
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		stack.append(utilities.fromBase(x, int(y)))
	#elif mode == 8: # list, str
	#elif mode == 9: # list, list
	else:
		dyadNotImplemented(mode, '')
"""
# Ḅ
def BLowDotOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append()
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3 or mode == 7: # num, list; list, num
		n = int(x if mode == 3 else y)
		l = y if mode == 3 else x

		result = []

		for i in l[::-1]:
			(n,r) = divmod(n, i)
			result.insert(0, r)
			if n == 0:
				break
		
		if n != 0:
			result.insert(0, n)

		stack.append(result)
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')
"""
# C
def COperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(-1 if x<y else (1 if x > y else 0))
	elif mode == 2 or mode == 4: # num, str; str, num
		n = str(x if mode == 2 else y)
		s = y if mode == 2 else x

		stack.append(s.count(n))
	elif mode == 3: # num, list
		stack.append(y.count(x))
	elif mode == 5: # str, str
		stack.append(x.count(y))
	elif mode == 6: # str, list
		stack.append(y.count(x))
	elif mode == 7: # list, num
		stack.append(x.count(y))
	elif mode == 8: # list, str
		stack.append(x.count(y))
	elif mode == 9: # list, list
		count = 0
		i = 0
		while i < len(x):
			if x[i:i+len(y)] == y:
				count += 1
				i += len(y)
			else:
				i += 1
		stack.append(count)
	else:
		dyadNotImplemented(mode, '')

# D
def DOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(abs(x-y))
	elif mode == 2 or mode == 4: # num, str; str num
		n = x if mode == 2 else y
		s = y if mode == 2 else x

		if s == "":
			stack.append("")
		else:
			index = (int(n)-1)%len(s)
			stack.append(s[:index]+s[index+1:])
	elif mode == 3 or mode == 7: # num, list; list, num
		n = x if mode == 3 else y
		l = y if mode == 3 else x

		if l == []:
			stack.append([])
		else:
			index = (int(n)-1)%len(l)
			stack.append(l[:index]+l[index+1:])
	elif mode == 5 or mode == 9: # str, str; list, list
		(x, y) = (list(x[:]), list(y[:]))
		for i in y:
			if i in x:
				x.remove(i)

		if mode == 5:
			x = ''.join(x)
		stack.append(x)
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	else:
		dyadNotImplemented(mode, '')

# E
def EOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x * 10**y)
	elif mode == 2 or mode == 4: # num, str; str, num
		n = x if mode < 4 else y
		s = list(y if mode < 4 else x)

		if len(s) == 0:
			stack.append(s)
		else:
			index = (int(n)-1)%len(s)

			v = s.pop(index)
			stack.append("".join(s))
			stack.append(v)
	elif mode == 3 or mode == 7: # num, list; list, num
		n = x if mode == 3 else y
		l = y if mode == 3 else x

		if len(l) == 0:
			stack.append(l)
		else:
			index = (int(n)-1)%len(l)

			v = l.pop(index)
			stack.append(l)
			stack.append(v)
	#elif mode == 5: # str, str
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		if x == []:
			stack.append([])
		else:
			x = x[:] # Deep copy x
			indices = [(int(utilities.castToNumber(i))-1)%len(x) for i in y]
			result = []

			for i in indices:
				result.append(x[i])
				x[i] = None

			while None in x:
				x.remove(None)

			stack.append(x)
			stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# Ė
def EHighDotOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if (x==0 and y==0) or (x % y == 0) else 0)
	elif mode == 2: # num, str
		x = str(x)
		stack.append(1 if x in y else 0)
	elif mode == 3: # num, list
		stack.append(1 if x in y else 0)
	elif mode == 4: # str, num
		y = str(y)
		stack.append(1 if y in x else 0)
	elif mode == 5: # str, str
		stack.append(1 if y in x else 0)
	elif mode == 6: # str, list
		stack.append(1 if x in y else 0)
	elif mode == 7: # list, num
		stack.append(1 if y in x else 0)
	elif mode == 8: # list, str
		stack.append(1 if y in x else 0)
	elif mode == 9: # list, list
		stack.append(1 if y in x else 0)
	else:
		dyadNotImplemented(mode, '')

# I
def IOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(round(x, y))
	elif mode == 2: # num, str
		x = str(x)
		stack.append(y.index(x)+1 if x in y else 0)
	elif mode == 3: # num, list
		stack.append(y.index(x)+1 if x in y else 0)
	elif mode == 4: # str, num
		y = str(y)
		stack.append(x.index(y)+1 if y in x else 0)
	elif mode == 5: # str, str
		stack.append(x.find(y)+1)
	elif mode == 6: # str, list
		stack.append(y.index(x)+1 if x in y else 0)
	elif mode == 7: # list, num
		stack.append(x.index(y)+1 if y in x else 0)
	elif mode == 8: # list, str
		stack.append(x.index(y)+1 if y in x else 0)
	elif mode == 9: # list, list
		if len(y)>len(x):
			stack.append(0)
		else:
			for i in range(len(x)):
				if x[i:i+len(y)]==y:
					stack.append(i+1)
					return
			stack.append(0)
	else:
		dyadNotImplemented(mode, '')

# K
def KOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		n = int(x)
		k = int(y)
		if k < 0 or k > n:
			stack.append(0)
		else:
			stack.append(math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
	#elif mode == 2: # num, str
	elif mode == 3 or mode == 7: # num, list
		n = int(x if mode == 3 else y)
		l = y if mode == 3 else x

		def subsets(l, n):
			if n > len(l) or n < 0:
				return []
			elif n == len(l):
				return [l]
			elif n == 0:
				return [[]]
			elif n == 1:
				return [[i] for i in l]
			else:
				result = []
				for i in range(len(l)-n+1):
					result += [[l[i]] + s for s in subsets(l[i+1:], n-1)]
				return result

		stack.append(subsets(l, n))
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		stack.append(''.join(c for c in x if c in y))
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append([i for i in x if i in y])
	else:
		dyadNotImplemented(mode, '')

# Ṁ
def MHighDotOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(max(x,y))
	#elif mode == 2: # num, str
	elif mode == 3 or mode == 7: # num, list; list, num
		n = x if mode == 3 else y
		l = y if mode == 3 else x

		n = int(n)%4
		l = [i if type(i) == list else [i] for i in l]

		for i in range(n):
			width = max(len(i) for i in l)
			l = [[e[j] for e in l[::-1] if len(e)>j] for j in range(width)]

		stack.append(l)
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		stack.append(max(x,y))
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(max(x,y))
	else:
		dyadNotImplemented(mode, '')

# Ṃ
def MLowDotOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(min(x,y))
	#elif mode == 2: # num, str
	elif mode == 3 or mode == 7: # num, list; list, num
		n = x if mode == 3 else y
		l = y if mode == 3 else x

		n = int(n)%4
		l = [i if type(i) == list else [i] for i in l]

		for i in range(n):
			width = max(len(i) for i in l)
			l = [[e[j] for e in l if len(e)>j] for j in range(width-1, -1, -1)]

		stack.append(l)
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		stack.append(min(x,y))
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		stack.append(min(x,y))
	else:
		dyadNotImplemented(mode, '')

# N
def NOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		x = int(x)
		y = int(y)
		if x == y:
			stack.append([])
		elif y < x:
			stack.append(list(range(x, y, -1)))
		else:
			stack.append(list(range(x, y)))
	#elif mode == 2: # num, str
	#elif mode == 3: # num, list
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		x = x[:]
		y = list(y[:])

		result = ""

		for i in x:
			if i in y:
				result += i
				y.remove(i)

		stack.append(result)
	#elif mode == 6: # str, list
	#elif mode == 7: # list, num
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		x = x[:]
		y = y[:]

		result = []

		for i in x:
			if i in y:
				result.append(i)
				y.remove(i)

		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# S
def SOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		(x,y) = (int(x), int(y))
		while y != 0:
			(x,y) = (y,x%y)
		stack.append(1 if x == 1 else 0)
	elif mode == 2 or mode == 3: # num, str; num, list
		stack.append([y[:int(x)], y[int(x):]])
	elif mode == 4 or mode == 7: # str, num; list, num
		stack.append([x[:int(y)], x[int(y):]])
	elif mode == 6 or mode == 8: # str, list; list, str
		l = x if mode == 8 else y
		s = y if mode == 8 else x

		if s in l:
			index = l.index(s)
			stack.append([l[:index], l[index+1:]])
		else:
			stack.append(l)
	elif mode == 5: # str, str
		s = x.split(y)
		stack.append([s[0], y.join(s[1:])])
	elif mode == 9: # list, list
		for i in range(len(x)):
			if x[i:i+len(y)] == y:
				stack.append([x[:i], x[i+len(y):]])
				return
		stack.append(x)
	else:
		dyadNotImplemented(mode, '')

# Ṡ
def SHighDotOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x ** (1/y)))
	elif mode == 2 or mode == 4 or mode == 3 or mode == 7: # num, str; str, num; num, list; list, num
		n = int(x if mode == 2 or mode == 3 else y)
		l = y if mode == 2 or mode == 3 else x

		stack.append([l[i:i+n] for i in range(len(l)-n+1)])
	elif mode == 5 or mode == 9: # str, str; list, list
		result = []
		start = 0

		for i in range(len(x)):
			if x[i] in y:
				result.append(x[start:i])
				start = i+1
		result.append(x[start:])
		stack.append(result)
	#elif mode == 6: # str, list
	#elif mode == 8: # list, str
	else:
		dyadNotImplemented(mode, '')

# U
def UOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		x = int(x)
		y = int(y)
		if x == y:
			stack.append([x])
		elif y < x:
			stack.append(list(range(x, y-1, -1)))
		else:
			stack.append(list(range(x, y+1)))
	#elif mode == 2: # num, str
	#elif mode == 3: # num, list
	#elif mode == 4: # str, num
	elif mode == 5: # str, str
		x = x[:]
		y = list(y[:])

		result = ""

		for i in x:
			if i in y:
				y.remove(i)

		stack.append(x + ''.join(y))
	#elif mode == 6: # str, list
	#elif mode == 7: # list, num
	#elif mode == 8: # list, str
	elif mode == 9: # list, list
		x = x[:]
		y = y[:]

		for i in x:
			if i in y:
				y.remove(i)

		stack.append(x+y)
	else:
		dyadNotImplemented(mode, '')

# Z
def ZOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x // y))
		stack.append(utilities.formatNum(x % y))
	elif mode == 2: # num, str
		result = []
		x = int(x)
		if x < 1 or x > len(y):
			raise ValueError("invalid size for unzipping: "+str(x))
		for i in range(x):
			index = i
			step = []
			while index < len(y):
				step.append(y[index])
				index += x
			result.append(''.join(step))
		stack.append(result)
	elif mode == 3: # num, list
		result = []
		x = int(x)
		if x < 1 or x > len(y):
			raise ValueError("invalid size for unzipping: "+str(x))
		for i in range(x):
			index = i
			step = []
			while index < len(y):
				step.append(y[index])
				index += x
			result.append(step)
		stack.append(result)
	elif mode == 4: # str, num
		result = []
		y = int(y)
		if y < 1 or y > len(x):
			raise ValueError("invalid size for unzipping "+str(y))
		for i in range(y):
			index = i
			step = []
			while index < len(x):
				step.append(x[index])
				index += y
			result.append(''.join(step))
		stack.append(result)
	elif mode == 5 or mode == 9: # str, str; list, list
		result = []
		minlen = min(len(x), len(y))
		for i in range(minlen):
			result.append(x[i])
			result.append(y[i])
		result += x[minlen:] + y[minlen:]
		if mode == 5:
			result = ''.join(result)
		stack.append(result)
	#elif mode == 6: # str, list
	elif mode == 7: # list, num
		result = []
		y = int(y)
		if y < 1 or y > len(x):
			raise ValueError("invalid size for unzipping "+str(y))
		for i in range(y):
			index = i
			step = []
			while index < len(x):
				step.append(x[index])
				index += y
			result.append(step)
		stack.append(result)
	#elif mode == 8: # list, str
	else:
		dyadNotImplemented(mode, '')

# ¤
def currencyOperator(stack, x, y, mode):
	if mode > 0:   # any types...
		stack.append(y)
		stack.append(x)
	else:
		dyadNotImplemented(mode, '')


#-- Extended Dyads -- #





"""
Blank operator function, just easy to copy-paste


# 
def ___Operator(stack, z, mode):
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		stack.append()
	else:
		monadNotImplemented(mode, '')


# 
def ___Operator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append()
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append()
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append()
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')

"""



"""
OPS DICT

Each value should be an Operator object
"""

ops = {
	# Nilads
	'€.': Operator('€.', 0, extDotOperator),
	'₵A': Operator('₵A', 0, constAOperator),
	'₵a': Operator('₵a', 0, constaOperator),
	'₵C': Operator('₵C', 0, constCOperator),
	'₵c': Operator('₵c', 0, constcOperator),
	'₵D': Operator('₵D', 0, constDOperator),
	'₵E': Operator('₵E', 0, constEOperator),
	'₵H': Operator('₵H', 0, constHOperator),
	'₵h': Operator('₵h', 0, consthOperator),
	'₵P': Operator('₵P', 0, constPOperator),
	'₵Q': Operator('₵Q', 0, constQOperator),
	'₵q': Operator('₵q', 0, constqOperator),
	'₵R': Operator('₵R', 0, constROperator),
	'₵r': Operator('₵r', 0, constrOperator),
	'₵V': Operator('₵V', 0, constVOperator),
	'₵v': Operator('₵v', 0, constvOperator),
	'₵W': Operator('₵W', 0, constWOperator),
	'₵X': Operator('₵X', 0, constXOperator),
	'₵x': Operator('₵x', 0, constxOperator),
	'₵Y': Operator('₵Y', 0, constYOperator),
	'₵y': Operator('₵y', 0, constyOperator),
	'∂A': Operator('∂A', 0, dateAOperator),
	'∂a': Operator('∂a', 0, dateaOperator),
	'∂D': Operator('∂D', 0, dateDOperator),
	'∂d': Operator('∂d', 0, datedOperator),
	'∂H': Operator('∂H', 0, dateHOperator),
	'∂h': Operator('∂h', 0, datehOperator),
	'∂I': Operator('∂I', 0, dateIOperator),
	'∂i': Operator('∂i', 0, dateiOperator),
	'∂K': Operator('∂K', 0, dateKOperator),
	'∂k': Operator('∂k', 0, datekOperator),
	'∂L': Operator('∂L', 0, dateLOperator),
	'∂l': Operator('∂l', 0, datelOperator),
	'∂M': Operator('∂M', 0, dateMOperator),
	'∂m': Operator('∂m', 0, datemOperator),
	'∂N': Operator('∂N', 0, dateNOperator),
	'∂n': Operator('∂n', 0, datenOperator),
	'∂O': Operator('∂O', 0, dateOOperator),
	'∂o': Operator('∂o', 0, dateoOperator),
	'∂Q': Operator('∂Q', 0, dateQOperator),
	'∂q': Operator('∂q', 0, dateqOperator),
	'∂S': Operator('∂S', 0, dateSOperator),
	'∂s': Operator('∂s', 0, datesOperator),
	'∂T': Operator('∂T', 0, dateTOperator),
	'∂t': Operator('∂t', 0, datetOperator),
	'∂U': Operator('∂U', 0, dateUOperator),
	'∂u': Operator('∂u', 0, dateuOperator),
	'∂W': Operator('∂W', 0, dateWOperator),
	'∂w': Operator('∂w', 0, datewOperator),
	'∂X': Operator('∂X', 0, dateXOperator),
	'∂x': Operator('∂x', 0, datexOperator),
	'∂Y': Operator('∂Y', 0, dateYOperator),
	'∂y': Operator('∂y', 0, dateyOperator),
	'∂Z': Operator('∂Z', 0, dateZOperator),
	'∂z': Operator('∂z', 0, datezOperator),
	'ø': Operator('ø', 0, emptySetOperator),
	'Ø': Operator('Ø', 0, emptyStringOperator),
	'₸': Operator('₸', 0, struckTOperator),
	'ℍ': Operator('ℍ', 0, struckHOperator),
	'¶': Operator('¶', 0, pilcrowOperator),
	'§': Operator('§', 0, sectionOperator),
	'@': Operator('@', 0, atOperator),
	# Monads
	'!': Operator('!', 1, exclamationOperator),
	'$': Operator('$', 1, dollarOperator),
	'(': Operator('(', 1, leftParenthesisOperator),
	')': Operator(')', 1, rightParenthesisOperator),
	':': Operator(':', 1, colonOperator),
	'b': Operator('b', 1, bOperator),
	'c': Operator('c', 1, cOperator),
	'd': Operator('d', 1, dOperator),
	'f': Operator('f', 1, fOperator),
	'g': Operator('g', 1, gOperator),
	'h': Operator('h', 1, hOperator),
	'i': Operator('i', 1, iOperator),
	'l': Operator('l', 1, lOperator),
	'n': Operator('n', 1, nOperator),
	'o': Operator('o', 1, oOperator),
	'p': Operator('p', 1, pOperator),
	'q': Operator('q', 1, qOperator),
	'r': Operator('r', 1, rOperator),
	's': Operator('s', 1, sOperator),
	't': Operator('t', 1, tOperator),
	'u': Operator('u', 1, uOperator),
	'v': Operator('v', 1, vOperator),
	'w': Operator('w', 1, wOperator),
	'y': Operator('y', 1, yOperator),
	'z': Operator('z', 1, zOperator),
	'\\': Operator('\\', 1, backslashOperator),
	'_': Operator('_', 1, underscoreOperator),
	'~': Operator('~', 1, tildeOperator),
	'…': Operator('…', 1, lowEllipsisOperator),
	'┅': Operator('┅', 1, highEllipsisOperator),
	'Σ': Operator('Σ', 1, sigmaOperator),
	'Π': Operator('Π', 1, piOperator),
	'‼': Operator('‼', 1, doubleExclamationOperator),
	'⌋': Operator('⌋', 1, floorOperator),
	'⌉': Operator('⌉', 1, ceilOperator),
	'Σ': Operator('Σ', 1, sigmaOperator),
	'ċ': Operator('ċ', 1, cHighDotOperator),
	'ḋ': Operator('ḋ', 1, dHighDotOperator),
	'ḍ': Operator('ḍ', 1, dLowDotOperator),
	'ė': Operator('ė', 1, eHighDotOperator),
	'ẹ': Operator('ẹ', 1, eLowDotOperator),
	'ḟ': Operator('ḟ', 1, fHighDotOperator),
	'ḣ': Operator('ḣ', 1, hHighDotOperator),
	'ḥ': Operator('ḥ', 1, hLowDotOperator),
	'ṁ': Operator('ṁ', 1, mHighDotOperator),
	'ṃ': Operator('ṃ', 1, mLowDotOperator),
	'ṅ': Operator('ṅ', 1, nHighDotOperator),
	'ṇ': Operator('ṇ', 1, nLowDotOperator),
	'ȯ': Operator('ȯ', 1, oHighDotOperator),
	'ọ': Operator('ọ', 1, oLowDotOperator),
	'ṗ': Operator('ṗ', 1, pHighDotOperator),
	'ṙ': Operator('ṙ', 1, rHighDotOperator),
	'ṛ': Operator('ṛ', 1, rLowDotOperator),
	'ṡ': Operator('ṡ', 1, sHighDotOperator),
	'ṣ': Operator('ṣ', 1, sLowDotOperator),
	'ṭ': Operator('ṭ', 1, tLowDotOperator),
	'ṫ': Operator('ṫ', 1, tHighDotOperator),
	'ụ': Operator('ụ', 1, uLowDotOperator),
	'ẋ': Operator('ẋ', 1, xHighDotOperator),
	'ẏ': Operator('ẏ', 1, yHighDotOperator),
	'ỵ': Operator('ỵ', 1, yLowDotOperator),
	'€|': Operator('€|', 1, extPipeOperator),
	'€[': Operator('€[', 1, extLeftBracketOperator),
	'€]': Operator('€]', 1, extRightBracketOperator),
	# Dyads
	'%': Operator('%', 2, percentOperator),
	'&': Operator('&', 2, ampersandOperator),
	'*': Operator('*', 2, asteriskOperator),
	'+': Operator('+', 2, plusOperator),
	',': Operator(',', 2, commaOperator),
	'/': Operator('/', 2, slashOperator),
	';': Operator(';', 2, semicolonOperator),
	'<': Operator('<', 2, lessThanOperator),
	'=': Operator('=', 2, equalsOperator),
	'>': Operator('>', 2, greaterThanOperator),
	'^': Operator('^', 2, caretOperator),
	'|': Operator('|', 2, pipeOperator),
	'«': Operator('«', 2, leftArrowQuoteOperator),
	'»': Operator('»', 2, rightArrowQuoteOperator),
	'⊂': Operator('⊂', 2, subsetOperator),
	'⊃': Operator('⊃', 2, supersetOperator),
	'∧': Operator('∧', 2, andOperator),
	'∨': Operator('∨', 2, orOperator),
	'⁻': Operator('⁻', 2, minusOperator),
	'×': Operator('×', 2, timesOperator),
	'÷': Operator('÷', 2, divisionOperator),
	'¤': Operator('¤', 2, currencyOperator),
	'B': Operator('B', 2, BOperator),
	#'Ḅ': Operator('Ḅ', 2, BLowDotOperator),
	'C': Operator('C', 2, COperator),
	'D': Operator('D', 2, DOperator),
	'E': Operator('E', 2, EOperator),
	'Ė': Operator('Ė', 2, EHighDotOperator),
	'I': Operator('I', 2, IOperator),
	'K': Operator('K', 2, KOperator),
	'N': Operator('N', 2, NOperator),
	'Ṁ': Operator('Ṁ', 2, MHighDotOperator),
	'Ṃ': Operator('Ṃ', 2, MLowDotOperator),
	'S': Operator('S', 2, SOperator),
	'Ṡ': Operator('Ṡ', 2, SHighDotOperator),
	'U': Operator('U', 2, UOperator),
	'Z': Operator('Z', 2, ZOperator)


}
