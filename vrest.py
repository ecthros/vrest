import requests
import base64
import logging
import json

from telegram import PassportElementErrorSelfie

class ServerParams():
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.server_port = 8697
        self.base_request_string = ("http://%s:%s/api" % (self.server_ip, self.server_port))

        self.headers = {"Authorization": ("Basic %s" % ""), "Content-type": "application/vnd.vmware.vmw.rest-v1+json", "Accept": "application/vnd.vmware.vmw.rest-v1+json"}

sp = ServerParams()

def check_response(response):
    if response.status_code == 401:
        logging.warning("Server returned unauthenticated error")
    elif response.status_code == 200:
        logging.info("Request successful.")
    elif response.status_code == 204:
        logging.info("Request successful, no output")
        return {}
    elif response.status_code == 404:
        logging.info("Request returned 404")
        return response.content
    else:
        logging.warning("Unknown status %d for request" % response.status_code)
    if response.content:
        return json.loads(response.content.decode("ascii"))
    else:
        return {}

def authenticate(user, password):
    ''' 
    Authenticates to the server. 
    Returns status code.
    '''
    authentication_string = base64.b64encode((user + ":" + password).encode('ascii'))
    sp.headers["Authorization"] = ("Basic %s" % authentication_string.decode('ascii'))
    
    response = requests.get(sp.base_request_string + "/vms", \
        headers=sp.headers)
    check_response(response)
    return response.status_code


def set_ip(ip_address):
    sp.server_ip = ip_address
    sp.base_request_string = ("http://%s:%s/api" % (sp.server_ip, sp.server_port))


def set_port(port):
    sp.server_port = port
    sp.base_request_string = ("http://%s:%s/api" % (sp.server_ip, sp.server_port))


# Host Networks Management

def get_vmnets():
    '''
    Returns all virtual networks
    Example: vrest.get_vmnets()
    '''
    response = requests.get(sp.base_request_string + "/vmnet", \
        headers=sp.headers)
    return check_response(response)

def get_vmnet_mactoip(vmnet):
    '''
    Returns all MAC-To-IP settings for DHCP service for a specific vmnet
    Example: vrest.get_vmnet_mactoip("vmnet8")
    '''
    response = requests.get(sp.base_request_string + "/vmnet/" + vmnet + "/mactoip", \
        headers=sp.headers)
    return check_response(response)

def get_vmnet_portforward(vmnet):
    '''
    Returns all port forwardings for a specific vmnet
    Example: vrest.get_vmnet_portforward("vmnet8")
    '''
    response = requests.get(sp.base_request_string + "/vmnet/" + vmnet + "/portforward", \
        headers=sp.headers)
    return check_response(response)

def update_vmnet_mactoip(vmnet, mac, params):
    '''
    Updates the Mac-To-IP binding for a specific vmnet
    Example: vrest.update_vmnet_mactoip("vmnet1", "00:00:00:00:00:00", {"IP": "125.5.5.5"})
    '''
    response = requests.put(sp.base_request_string + "/vmnet/" + vmnet + "/mactoip/" + mac, \
        headers=sp.headers, json=params)
    return check_response(response)

def update_portforward(vmnet, protocol, port, params):
    '''
    Updates Port Forwarding for a specific vmnet
    Example: vrest.update_portforward("vmnet8", "tcp", "50000", {"ip": "192.168.1.128", "port": 40000, "desc": "test rule"})
    '''
    response = requests.put(sp.base_request_string + "/vmnet/" + vmnet + "/portforward/" + protocol + "/" + str(port), \
        headers=sp.headers, json=params)
    return check_response(response)

def create_vmnet(params):
    '''
    Creates a new VMNet.
    Possible values:
        "name": "string"
        "type": "bridged"
        "dhcp": "true"
        "subnet": "string"
        "mask": "string"
    Example: response = vrest.create_vmnet({"name": "Test VMNet"})
    '''
    response = requests.post(sp.base_request_string + "/vmnets", \
        headers=sp.headers, json=params)
    return check_response(response)

def delete_portforward(vmnet, protocol, port):
    '''
    Deletes a port forwarding rule.
    Example: vrest.delete_portforward("vmnet8", "tcp", "40000")
    '''
    response = requests.delete(sp.base_request_string + "/vmnet/" + vmnet + "/portforward/" + protocol + "/" + port, \
        headers=sp.headers)
    return check_response(response)

# VM Management

def get_vms():
    '''
    Returns a list of VM IDs and paths for all VMs
    Example: vrest.get_vms()
    '''
    response = requests.get(sp.base_request_string + "/vms", \
        headers=sp.headers)
    return check_response(response)

def get_vm(vm_id):
    '''
    Returns the VM Settings for a VM
    Example: vrest.get_vm("CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M")
    '''
    response = requests.get(sp.base_request_string + "/vms/" + vm_id, \
        headers=sp.headers)
    return check_response(response)

def get_vm_config(vm_id, params):
    '''
    Returns the VM Config for a VM
    Example: vrest.get_config("CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M", "string")
    '''
    response = requests.get(sp.base_request_string + "/vms/" + vm_id + "/params/" + params, \
        headers=sp.headers)
    return check_response(response)

def get_vm_restrictions(vm_id):
    '''
    Returns the VM restrictions information
    Example: vrest.get_vm_restrictions("CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M")
    '''
    response = requests.get(sp.base_request_string + "/vms/" + vm_id + "/restrictions", \
        headers=sp.headers)
    return check_response(response)

def update_vm(vm_id, params):
    '''
    Updates the VM Settings
    Example: vrest.update_vm("CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M", {"memory":4096})
    '''
    response = requests.put(sp.base_request_string + "/vms/" + vm_id, \
        headers=sp.headers, json=params)
    return check_response(response)

def update_vm_config(vm_id, params):
    '''
    Updates the VM Config parameters
    Example: vrest.update_vm_config("CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M", {"memory":4096})
    '''
    response = requests.put(sp.base_request_string + "/vms/" + vm_id + "/configparams", \
        headers=sp.headers, json=params)
    return check_response(response)

def copy_vm(params):
    '''
    Creates a copy of the given VM.
    Example: vrest.copy_vm({"id": "CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M", "cpu": {"processors": 1},
        "memory": 512, "name": "New VM", "parentID": "CCOAEHSK2ASF5S5FAS3TQN3TO2CGFJ6M"})
    '''
    response = requests.post(sp.base_request_string + "/vms", \
        headers=sp.headers, json=params)
    return check_response(response)

def register_vm(params):
    '''
    Registers a VM to the VM library.
    Example: vrest.register_vm({"id": 'R00MBA5HVMN0L3SULC0DQMDSL6TSO3CE', "path": "C:\\Users\\georg\\Downloads\\cp7_30_22\\cpxv_exrd_e_ubu16\\cpxv_exrd_e_ubu16\\cpxv_exrd_e_ubu16.vmx", "name": "New VM"})
    '''
    response = requests.post(sp.base_request_string + "/vms/registration", \
        headers=sp.headers, json=params)
    return check_response(response)

def delete_vm(vm_id):
    '''
    Deletes a VM
    Example: vrest.delete_vm('4FK20QNKTVHGNSEF2GLJ86MOA7C63559')
    '''
    response = requests.delete(sp.base_request_string + "/vms/" + vm_id, \
        headers=sp.headers)
    return check_response(response)

# VM Network Adapters Management

def get_ip(vm_id):
    pass

def get_nics(vm_id):
    pass

def update_nic(vm_id, index, params):
    pass

def create_nic(vm_id, params):
    pass

def delete_nic(vm_id, index):
    pass

# VM Power Management

def get_power(vm_id):
    pass

def update_power(vm_id, params):
    pass

# VM Shared Folders Management

def get_sharedfolders(vm_id):
    pass

def update_sharedfolder(vm_id, folder_id, params):
    pass

def create_sharedfolder(vm_id, params):
    pass

def delete_sharedfolder(vm_id, folder_id):
    pass


authenticate("georg", "qwe123QWE!@#")
print("Authenticated to server.")