from itertools import permutations

def solve_cryptarithmetic():
    letters = 'SENDMORY'
    digits = range(10)
    for perm in permutations(digits, len(letters)):
        assign = dict(zip(letters, perm))
        if assign['S'] == 0 or assign['M'] == 0:
            continue
        send = assign['S']*1000 + assign['E']*100 + assign['N']*10 + assign['D']
        more = assign['M']*1000 + assign['O']*100 + assign['R']*10 + assign['E']
        money = assign['M']*10000 + assign['O']*1000 + assign['N']*100 + assign['E']*10 + assign['Y']
        if send + more == money:
            return assign, send, more, money

solution, send, more, money = solve_cryptarithmetic()
print(f"SEND: {send}, MORE: {more}, MONEY: {money}")
print("Assignment:", solution)
