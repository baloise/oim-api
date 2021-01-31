from ourCloud import ourCloud

# Create an instance of the ourCloud class that can be used within this scope
oc = ourCloud()


def tokendemo():
    # This function is called by the api endpoint defined in
    # oimtest.yaml found in the openapi/ folder
    return str(oc.auth.getToken())
