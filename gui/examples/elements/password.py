#!/usr/bin/python
# -*- coding: utf-8 -*- #
import bcrypt


password = b'superpuper'
hashed = bcrypt.hashpw(password, bcrypt.gensalt())


def check(inputed_pw):
    return bcrypt.hashpw(inputed_pw, hashed) == hashed


def main():
    inputed = raw_input('Input password: ')
    print 'Matched' if check(inputed) else 'Ooops'


if __name__ == "__main__":
    main()
