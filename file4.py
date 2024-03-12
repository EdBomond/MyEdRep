nums=list(range(2,110,5))
for n in nums:
    print(n)
sq=[]   
for t in range(1,101):
    sq.append(t**2)
print(sq)
print(f"{min(sq)} {max(sq)} {sum(sq)}")
sd=[val*2 for val in range(1,101,2)]
print(sd[-15:])
fg=nums[:]
print(fg)
nums.pop()
print(fg)
if 5 in fg:
    print("true")
else:
    print("false")    
