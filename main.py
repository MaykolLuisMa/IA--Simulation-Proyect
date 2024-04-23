#dependencias
from nlp.nlp import *
import os
from program import INFORM

#visual
while(True):
    query = input('Enter your query:\n')
    os.system('clear')
    print('Loading...')
    result = response(INFORM, query)
    os.system('clear')
    print('RESULTS:')
    print(result)
    print('')
    input('Press "enter" to make another query...\n')
    os.system('clear')
