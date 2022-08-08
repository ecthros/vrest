Turns out the VMWare Workstation has a REST API where you can do a bunch of cool stuff. This repo contains python bindings to make it easier to call the REST functions.

Unfortunately, the server doesn't start by default; you have to start it yourself. To do this, navigate to the folder where VMWare is installed and run `vmrest -C` (to set up the credential) and then `vmrest`:

1. C:\Program Files (x86)\VMware\VMware Workstation>vmrest -C
  <Enter new credentials>
2. C:\Program Files (x86)\VMware\VMware Workstation>vmrest

When using this script, make sure to call vrest.authenticate(user, password) to set your username and password accordingly. You can also change the IP or port with vrest.set_ip(ip) or vrest.set_port(port).
