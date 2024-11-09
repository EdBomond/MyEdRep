import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

xCH  = [0,0,0,0,0,0,1,1,0,0,0,0]
xCH2 = [0,1,2,3,4,0,2,2,1,3,4,5]
xCH3 = [2,2,2,2,2,4,3,3,4,1,1,1]
xCl  = [0,0,0,0,0,0,0,0,0,1,1,1]
exp  = [5.16,14.79,21.62,26.43,31.56,21.84,29.89,30.27,27.69,33.51,38.24,42.83]

print(f"{len(xCH)}, {len(xCH2)}, {len(xCH3)}, {len(xCl)}, {len(exp)}")
df=pd.DataFrame([xCH,xCH2,xCH3,xCl,exp])
print(df)
data = {'xCH':  [0,0,0,0,0,0,1,1,0,0,0,0],
        'xCH2': [0,1,2,3,4,0,2,2,1,3,4,5],
        'xCH3': [2,2,2,2,2,4,3,3,4,1,1,1],
        'xCl':  [0,0,0,0,0,0,0,0,0,1,1,1],
        'exp':  [5.16,14.79,21.62,26.43,31.56,21.84,29.89,30.27,27.69,33.51,38.24,42.83]}

df=pd.DataFrame(data)

dftr=pd.DataFrame([xCH,xCH2,xCH3,xCl,exp]).transpose()

print(dftr)

Y=df['exp'].values
print(Y)
X=df[['xCH','xCH2','xCH3','xCl']]
print(X)
X.shape[0]
nf=np.ones((X.shape[0],1))
print(nf)
X=np.hstack((np.ones((X.shape[0],1)),X))
print(X)
X_t=X.T
print(X_t)
npdot=np.dot(X_t,X)
print(npdot)
z=np.linalg.inv(npdot)
print(z)
z1=np.dot(z,X_t)
print(z1)
A=np.dot(z1,Y)
print(A)
df['exp_cals']=df['xCH']*A[1]+df['xCH2']*A[2]+df['xCH3']*A[3]+df['xCl']*A[4]+A[0]

print(df)
ax=df.plot.scatter(x='exp', y='exp_cals',figsize=(10,10),color='red')
pd.DataFrame([[df['exp'].min(),df['exp'].min()],[df['exp'].max(),df['exp'].max()]]).plot(x=0,y=1,ax=ax,legend=False)
plt.show()