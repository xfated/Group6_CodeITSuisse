import logging
import json
from itertools import zip_longest
from os import path
import enchant

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored():

    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    inputs = data['inputs']
    output = []
    
    def findpalin(s):
        longest = ""
        for i in binRange(1,len(s)-1):
            if min(i,len(s)-i)*2+1 <= len(longest): continue
            for odd in [1,0]:
                if s[i+odd] != s[i-1]: continue
                halfSize = len(path.commonprefix([s[i+odd:],s[:i][::-1]])) 
                if 2*halfSize + odd > len(longest):
                    longest = s[i-halfSize:i+halfSize+odd];break
        return longest

    def binRange(lo,hi=None):
        if hi is None: lo,hi = 0,lo
        if hi <= lo: return
        mid = (lo+hi-1)//2
        yield mid
        for a,b in zip_longest(binRange(lo,mid),binRange(mid+1,hi),fillvalue=None):
            if a is not None: yield a
            if b is not None: yield b

    def brute(m):
        d = enchant.Dict("en_US")
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'
        for key in range(len(LETTERS)):
            translated = ''
            for symbol in m:
                if symbol in LETTERS:
                    num = LETTERS.find(symbol)
                    num = num - key

                    if num < 0:
                        num += len(LETTERS)
                    translated += LETTERS[num]

                else:
                    translated += symbol

            if d.check(translated):
                return translated, key 

    for i in inputs:
        message = i['encryptedText']
        id_num = i['id']
        decrypt = {}

        longest_palin = findpalin(message)              #find longest palindrome
        solve, key = brute(longest_palin)               #find the word and key 





