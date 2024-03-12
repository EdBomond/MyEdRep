alien_0={"color" : "green", "point" : 5}
print(alien_0["color"])
print(alien_0["point"])
alien_0['x_position']=0
alien_0['y_position']=35
alien_0["nums"]=list(range(2,110,5))
print(alien_0["nums"])
setting={
    "key1":"set1",
    "key2":"set2",
    "key3":"set3",
    "key4":"set4",
    "key5":"set5"
    }
for key,val in setting.items():
    print(f"{key} - {val}")
lang=["c","python","c++","ruby","cobol"]
fav_lang={
    "ed":lang[2],
    "sanya":lang[4],
    "igor":lang[0],
    "lena":lang[0],
    "petr":"None"
}
for key in fav_lang:
    print(f"{key} - {fav_lang[key]}")
for val in set(fav_lang.values()):
    print(f"{val}")
