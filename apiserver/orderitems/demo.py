from ourCloud import ourCloud

oc = ourCloud()

def tokendemo():
    return str(oc.auth.getToken())
