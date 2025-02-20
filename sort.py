import random

def listA(n):
  lis=[]
  for i in range(0,n):
    lis.append(random.randint(1, 1000000))
  return lis


def tournament_two(A):
 N = len(A)
 winner = [None] * (N-1)
 loser = [None] * (N-1)
 prior = [-1] * (N-1)
 idx = 0
 for i in range(0, N, 2):
  if A[i] < A[i+1]:
    winner[idx] = A[i+1]
    loser[idx] = A[i]
  else:
    winner[idx] = A[i]
    loser[idx] = A[i+1]
  idx += 1
 m = 0
 while idx < N-1:
  if winner[m] < winner[m+1]: 
    winner[idx] = winner[m+1]
    loser[idx] = winner[m]
    prior[idx] = m+1
  else:
    winner[idx] = winner[m]
    loser[idx] = winner[m+1]
    prior[idx] = m
  m += 2
  idx += 1
 largest = winner[m]
 second = loser[m]
 m = prior[m]
 while m >= 0:
   if second < loser[m]: 
     second = loser[m]
   m = prior[m]
 return (largest, second)

r=listA(500)
print(r)

print(tournament_two(r))