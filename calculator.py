from collections import deque
from itertools import cycle
import re


NUMBER = "(\d+\.*\d*)" 
OPERATIONS = deque(('-', '+', '/', '*', '**'))


def no_whitespace(message: str) -> str:
    return re.sub("\s+", "", message)


def result(a: [int, float], b: [int, float], op: str) -> float:
    if op == '**': return a ** b
    elif op == '*': return a * b
    elif op == '/': return a / b
    elif op == '+': return a + b
    elif op == '-': return a - b
    else: raise ValueError(f"Unrecognized operation {operation}")


def calculator(message: str) -> float:
    message = no_whitespace(message)
    while operations:
        operation = operations.pop()
        regex = f"({NUMBER}){operation}({NUMBER})"
        search = re.search(regex, message)
        while search:
            re.sub(regex, result(*map(float, search.groups), operation), message)
            search = re.search(regex, message)
