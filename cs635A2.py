
'''
This program implements a recursive descent parser for the CFG below:

The grammar has added pi and unary minus to the previous program.
Also, the parse function is now called in a loop, so you can evaluate
one expression after another.
------------------------------------------------------------
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → <number> | (<exp>) |<func>
4 <func> → <func name>(<exp>)
5 <func name> → sin | cos | tan | exp | sqrt | abs

'''
import math

class ParseError(Exception): pass

#==============================================================
# FRONT END PARSER
#==============================================================

i = 0 # keeps track of what character we are currently reading.
err = None
#---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value
#---------------------------------------
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
#---------------------------------------
# Parse a Factor   <factor> → <number> | pi | -<factor> | (<exp>)
#       
def factor():
    global i, err
    value = None
    
    if w[i] == 'pi':
        i += 1
        return math.pi
    elif w[i] == '-':
        i += 1
        return -factor()
    elif w[i] == '(':
        i += 1
        temp = exp()
        if w[i] == ')':
            i += 1
            return temp
        else:
            print('you need ) to complete')
            raise ParseError
    elif w[i] == funcname(w[i]):
        i += 1
        value = func()

    # elif w[i] =='sin' or 'cos' or 'tan' or 'exp' or 'sqrt' or 'abs':
    #     i+=1
    #     return func()

    else:
        try:
            value = atomic(w[i])
            i += 1          # read the next character
        except ValueError:
            print('number expected')
            value = None
    
    #print('factor returning', value)
    
    if value == None: raise ParseError
    return value
#---------------------------------------
# Parse a Fuction   <func> → <func name>(<exp>)
#
def func():
    global  i, err
    value = fuc_call(funcname(w[i-1]), exp())
    return value


# ---------------------------------------
# Parse a Fuction name   <func name> → sin | cos | tan | exp | sqrt | abs
#
def funcname(expv):
    global i; err
    if expv == 'sin':
        return 'sin'
    elif expv == 'cos':
        return 'cos'
    elif expv == 'tan':
        return 'tan'
    elif expv == 'exp':
        return 'exp'
    elif expv == 'sqrt':
        return 'sqrt'
    elif expv == 'abs':
        return 'abs'
    else:
        return None
#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================
def binary_op(op, lhs, rhs):
    if op == '+': return lhs + rhs
    elif op == '-': return lhs - rhs
    elif op == '*': return lhs * rhs
    elif op == '/': return lhs / rhs
    else: return None

 
def atomic(x):
    return float(x)


def fuc_call(func_name, exp_value):
    if func_name == 'sin': return math.sin(exp_value)
    elif func_name == 'cos': return math.cos(exp_value)
    elif func_name == 'tan': return math.tan(exp_value)
    elif func_name == 'exp': return math.exp(exp_value)
    elif func_name == 'sqrt': return math.sqrt(exp_value)
    elif func_name == 'abs': return math.abs(exp_value)
    else: return None

#==============================================================
# User Interface Loop
#==============================================================
w = input('\nEnter expression: ')
while w != '':
    #------------------------------
    # Split string into token list.
    #
    for c in '()+-*/':
        w = w.replace(c, ' '+c+' ')
    w = w.split()
    w.append('$') # EOF marker

    print('\nToken Stream:     ', end = '')
    for t in w: print(t, end = '  ')
    print('\n')
    i = 0
    try:
        print('Value:           ', exp()) # call the parser
    except:
        print('parse error')
    print()
    if w[i] != '$': print('Syntax error:')
    print('read | un-read:   ', end = '')
    for c in w[:i]: print(c, end = '')
    print(' | ', end = '')
    for c in w[i:]: print(c, end = '')
    print()
    w = input('\n\nEnter expression: ')
#print(w[:i], '|', w[i:])

