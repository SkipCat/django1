from django.shortcuts import render
from django.http import HttpResponse
import math
import sys

def index(request):
    rule = request.GET.get('rule', None)

    if rule is None:
        return HttpResponse('Please provide a parameter in URL like "?rule=<number>"')
    else:
        return HttpResponse('<pre>' + automaton(rule) + '</pre>')

def automaton(ruleNumber):
    rule = [int(i) for i in f'{int(ruleNumber):08b}']
    
    first_line = [0 for number in range(79)]
    first_line[round(len(first_line) / 2) - 1] = 1

    lines = []
    lines.append(first_line)
    line_count = 1

    while line_count < 40:
        new_line = []
        previous_line = lines[-1]
        
        for i, _ in enumerate(previous_line):
            # check for left border
            if i - 1 < 0:
                previous_value = 0
            else:
                previous_value = previous_line[i - 1]
            
            # check for right border
            if i + 1 > len(previous_line) - 1:
                next_value = 0
            else:
                next_value = previous_line[i + 1]
            
            if previous_value == 1 and previous_line[i] == 1 and next_value == 1:
                new_line.append(rule[0])
            elif previous_value == 1 and previous_line[i] == 1 and next_value == 0:
                new_line.append(rule[1])
            elif previous_value == 1 and previous_line[i] == 0 and next_value == 1:
                new_line.append(rule[2])
            elif previous_value == 1 and previous_line[i] == 0 and next_value == 0:
                new_line.append(rule[3])
            elif previous_value == 0 and previous_line[i] == 1 and next_value == 1:
                new_line.append(rule[4])
            elif previous_value == 0 and previous_line[i] == 1 and next_value == 0:
                new_line.append(rule[5])
            elif previous_value == 0 and previous_line[i] == 0 and next_value == 1:
                new_line.append(rule[6])
            else:
                new_line.append(rule[7])
            
        lines.append(new_line)
        line_count += 1

    buffer = []

    for line in lines:
        line_schema = ''

        for value in line:
            if value == 1:
                buffer.append("#")
            else:
                buffer.append(".")
        
        buffer.append("\n")
    
    return ''.join(buffer)
