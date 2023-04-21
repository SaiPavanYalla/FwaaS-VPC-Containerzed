import os
import json
import ipaddress
import subprocess
import time

# get the current working directory
cwd = os.getcwd()

# Navigate to the parent directory of south_bound
parent_dir = os.path.dirname(cwd)

# Navigate to the Network directory
network_json_file_path  = os.path.join(parent_dir, "north_bound", "Infrastructure","infrastructure.json")

# Open the file for reading
with open(network_json_file_path, 'r') as f:
    network_data = json.load(f)


def reachibility_check(ip_address):
    host = ip_address
    fail_count = 0
    status = True
    
    while True:
        if subprocess.call(['ping', '-c', '1', host]) == 0:
            break
        else:
            fail_count += 1
            
        
        if fail_count == 5:
            status = False
            print("Health check failed for "+ host)
            break
                
    

    return status



def delete_container(hostname,namespace_tenant):
    inventory_path = os.path.join(cwd, "inventory.ini")
    playbook_path = os.path.join(cwd, "ansible_scripts","delete_container.yml")
    
    extra_vars = {'namespace_tenant': namespace_tenant , 'hostname': hostname  }
    command = ['sudo','ansible-playbook', playbook_path ,'-i', inventory_path]
    sudo_password = "csc792"

    for key, value in extra_vars.items():
        command.extend(['-e', f'{key}={value}'])

    status = "Delete"
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = process.communicate(sudo_password.encode())

    if process.returncode != 0:
        output = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
        status = "Delete"
        #print(f"Ansible playbook failed with error while deleting a Firewall:\n{output}")
    else:
        
        status = "Deleted"
        #print(f" The External network {vm_net_name} for Master Firewall  has been successfully created in {namespace_tenant}.")

    return status

       




for tenant in  network_data:

    if  "Firewall" in network_data[tenant].keys():
        firewall_data = network_data[tenant]["Firewall"]
        status_master = "Delete"
        if "Firewall_master" in firewall_data.keys():
            if firewall_data["Firewall_master"]["status"]["firewall_status"] == "Completed":
                ip=firewall_data["Firewall_master"]["ip_address"]
                if(not reachibility_check(ip)):
                    status_master = delete_container("FW1",tenant)
                    if status_master == "Deleted":

                        firewall_data["Firewall_master"]["status"]["firewall_status"] = "Ready"
                        firewall_data["Firewall_master"]["status"]["internal_net_attach_status"] = "Ready"
                        firewall_data["Firewall_master"]["status"]["external_net_attach_status"] = "Ready"
                        firewall_data["Firewall_master"]["status"]["mgmt_net_attach_status"] = "Ready"
                        firewall_data["Firewall_master"]["status"]["fw_control_plane"] = "Ready"
                        firewall_data["Firewall_master"]["status"]["vrrp_status"] = "Ready"
                        
                    
                    

        if "Firewall_backup" in firewall_data.keys():
            if firewall_data["Firewall_backup"]["status"]["firewall_status"] == "Completed":
                ip=firewall_data["Firewall_backup"]["ip_address"]
                if( not reachibility_check(ip)):
                    status_backup = delete_container("FW1",tenant)
                    if status_backup == "Deleted":

                        firewall_data["Firewall_backup"]["status"]["firewall_status"] = "Ready"
                        firewall_data["Firewall_backup"]["status"]["internal_net_attach_status"] = "Ready"
                        firewall_data["Firewall_backup"]["status"]["external_net_attach_status"] = "Ready"
                        firewall_data["Firewall_backup"]["status"]["mgmt_net_attach_status"] = "Ready"
                        firewall_data["Firewall_backup"]["status"]["fw_control_plane"] = "Ready"
                        firewall_data["Firewall_backup"]["status"]["vrrp_status"] = "Ready"
        
        if status_backup == "Deleted" or status_master == "Deleted":
            if "Policies" in in firewall_data.keys():
                for policy in firewall_data["Policies"].items():
                    policy["status"] = "Ready"



with open(network_json_file_path, "w") as outfile:
    # write the JSON data to the file
    json.dump(network_data, outfile,indent=4)    