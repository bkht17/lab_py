def is_palindrome(s):
    s = ''.join(char.lower() for char in s)
    checker = (s == s[::-1])
    return checker

x = str(input())
print(is_palindrome(x))
