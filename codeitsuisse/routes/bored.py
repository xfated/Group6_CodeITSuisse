import logging
import json
from itertools import zip_longest
from os import path

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
# setofwords = set(words.words())
from nltk.corpus import words
setofwords = set(words.words())


@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored():

    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    inputs = data
    output = []
    
    def findpalin(s):
        # longest = ""
        # for i in binRange(1,len(s)-1):
        #     if min(i,len(s)-i)*2+1 <= len(longest): continue
        #     for odd in [1,0]:
        #         if s[i+odd] != s[i-1]: continue
        #         halfSize = len(path.commonprefix([s[i+odd:],s[:i][::-1]])) 
        #         if 2*halfSize + odd > len(longest):
        #             longest = s[i-halfSize:i+halfSize+odd];break
        # return longest
        palins = []
        # odd lengths
        for mid in range(1,len(s)-1):
            # consider = False
            temp = s[mid]
            for dist in range(1, int((len(s)+1)/2)):
                start, end = mid-dist, mid+dist
                if start >= 0 and end < len(s):
                    if s[start] == s[end]:
                        temp = s[start] + temp + s[end]
                        palins.append(temp)
                    #     consider = True
                    else:
                    #     if consider == True:
                    #         palins.append(temp)
                        break
                # elif start == -1 or end == len(s):
                #     if consider == True:
                #         palins.append(temp)
        # even lengths
        for mid in range(0,len(s)-1):
            # consider = False
            temp = ''
            for dist in range(0, int((len(s)+1)/2)):
                start, end = mid-dist, mid+1+dist
                if start >= 0 and end < len(s):
                    if s[start] == s[end]:
                        temp = s[start] + temp + s[end]
                        palins.append(temp)
                #         consider = True
                    else:
                #         if consider == True:
                #             palins.append(temp)
                        break
                # elif start == -1 or end == len(s):
                #     if consider == True:
                #         palins.append(temp)
        palins = sorted(palins, key=len)
        return palins
    
    def sumString(s):
        return sum([ord(char) for char in s])
        
    def checkSentence(s):#, dict):
        for i in range(4,len(s)):
            for j in range(0, len(s)-i):
                # if s[j:j+i] in setofwords:
                #     print('sentence', s[j:i+1])
                #     return True
                print(s[j:j+i])
                if s[j:j+i] in setofwords:
                    print(s[j:j+i])
                    return True
        else:
            return False
        # count = 0
        # vowels = ['a','e','i','o','u']
        # for char in s:
        #     if s in vowels:
        #         count += 1
        # if count >= len(s)/4:
        #     return True
        # else:
        #     return False
    
    def shift(s, shift):
        data = []
        for i in range(len(s)):
            data.append(chr((ord(s[i])+shift-97)%26+97))           
        output = ''.join(data)
        return output

    # def binRange(lo,hi=None):
    #     if hi is None: lo,hi = 0,lo
    #     if hi <= lo: return
    #     mid = (lo+hi-1)//2
    #     yield mid
    #     for a,b in zip_longest(binRange(lo,mid),binRange(mid+1,hi),fillvalue=None):
    #         if a is not None: yield a
    #         if b is not None: yield b

    # def brute(m):
    #     d = enchant.Dict("en_US")
    #     LETTERS = 'abcdefghijklmnopqrstuvwxyz'
    #     for key in range(len(LETTERS)):
    #         translated = ''
    #         for symbol in m:
    #             if symbol in LETTERS:
    #                 num = LETTERS.find(symbol)
    #                 num = num - key

    #                 if num < 0:
    #                     num += len(LETTERS)
    #                 translated += LETTERS[num]

    #             else:
    #                 translated += symbol

    #         if d.check(translated):
    #             return translated, key 

    for i in inputs:
        message = i['encryptedText']
        id_num = i['id']
        decrypt = {}
        
        originalText = ''
        # dict_en = enchant.Dict("en_US")
        # longest_palin = findpalin(message)              #find longest palindrome
        # solve, key = brute(longest_palin)               #find the word and key 
        
        isValid = False
        palins = findpalin(message)
        numPalins = len(palins)

        encrpytionCount = 0    
        new_message = message
        if numPalins == 0:
            while isValid == False:
                # final_letter = new_message[0]
                for i in range(1, 26):
                    print(i)
                    temp = shift(new_message,i)
                    initial_letter = temp[0]
                    desired_shift = (ord(initial_letter) - 97 % 26)
                    # desired_shift = abs(ord(final_letter) - ord(initial_letter))
                    if desired_shift == 26 - i:
                        encryptionCount += 1
                        new_message = temp
                        if checkSentence(new_message) == True:
                            isValid = True
                        break
        else:
            longestPalin = palins[-1]
            while isValid == False:
                for i in range(1,26):
                    temp = shift(new_message,i)
                    initLongestPalin = shift(longestPalin, i)
                    desired_shift = (sumString(initLongestPalin) + numPalins)%26
                    if desired_shift == 26 - i:
                        encrpytionCount += 1
                        new_message = temp
                        longestPalin = initLongestPalin    
                        if checkSentence(new_message) == True:
                            isValid = True 
                        # if 'racecar' in new_message:
                        #     print("RACECAR")
                        break
        originalText = new_message
        # while checkSentence(message,dict_en) == False:
        #     message = shift(message, 1)
        #     print(message)
        # originalText = message

        # encrpytionCount = 1

        answer = {}
        answer['id'] = id_num
        answer['encrpytionCount'] = encrpytionCount
        answer['originalText'] = originalText
        output.append(answer)
        
    logging.info("My result :{}".format(output))
    return json.dumps(output)



