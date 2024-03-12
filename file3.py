bicycles=["trek","redline","cannon","biterk"]
print(bicycles[-1])
bicycles[-1]="motobike"
bicycles.append("fiat")
for bi in bicycles:
  print(bi.title())
schet=[]
for bi in bicycles:
  schet.append(bi.title())
schet.insert(2,"honda")  
print(schet)
schet.sort(reverse=True)
print(schet)
bi2=bicycles.remove("fiat")
print(sorted(bicycles))
schet.reverse()
print(len(schet))
print(bi2)
print(schet[len(schet)-1])