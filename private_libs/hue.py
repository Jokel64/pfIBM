from phue import Bridge

b = Bridge('ip_of_your_bridge')

b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()