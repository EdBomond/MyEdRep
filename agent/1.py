import winapps

for app in winapps.list_installed():
    print(app)
    print(app.name)
    print(app.version)
    print(app.install_date)
    
