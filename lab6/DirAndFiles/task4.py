import os

def count_lines(file):
    with open(file, 'r') as couunter:
        lines = len(couunter.readlines())
        print('Number of lines:', lines)

count_lines("/Users/bakhyt17/Documents/github-recovery-codes.txt")