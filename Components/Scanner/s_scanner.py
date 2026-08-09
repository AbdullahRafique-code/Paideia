# This is our nmap integrate network scanner but without the nmap dependency. It uses the socket library to scan for open ports on a given host.

import subprocess
import xml.etree.ElementTree as ET
import json 

# Function to run nmap scan and return the results in XML format
def run_network_scan(target_subnet):
    # it runs the nmap command with the specified target subnet and outputs the results in XML format
    # for specfic ports   
    print(f"Running nmap scan on {target_subnet}...")
    nmap_cmd=["nmap","-n","-sS","-sV","--open",
              "-T4","--max-retries","3","--host-timeout","2m", # new flags to speed up the scan and reduce the number of retries and timeout for each host
        "-p","23,80,443,554,161,8000,8080,8443,37777,35000", # ports to scan for
        "-oX","-",target_subnet]

    # response schema
    response_schema={
        "status":"success",
        "error":None,
        "discovered_devices":[]
    }

    try:
        # Run the nmap command and capture the output (raw byte stream)
        # in a pipe to be processed later, rather than displaying on screen
        # 
        cmd_result=subprocess.run(nmap_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        if cmd_result.returncode != 0: #failed to run nmap command
            # extracting the error message
            err_text=cmd_result.stderr.decode('utf-8').strip()
             #check if the error is because of lack of root privileges,
            if "requires root" in err_text.lower() or "privileges" in err_text.lower():
                err_text="error:Nmap requires root privileges to run. Please run the script as root/Admin."

            response_schema["status"]="failed"
            response_schema["error"]=err_text
            return json.dumps(response_schema,indent=2)
                

        # Parse the XML output from nmap into a DOM tree in Mem
        root=ET.fromstring(cmd_result.stdout)
        discovered_devices=[]

        # Traverse the XML tree to extract information about each host
        for host in root.findall('host'):
            #ensuring host is up
            status=host.find('status')
            if status.get('state') != 'up':
                continue

            # ip address and mac address are initialized to None and Unknown respectively, in case they are not found in the XML output
            # ip is None so that we can check if it was found or not (skip if not found), and mac is set to 'Unknown' as a default value
            ip_address=None
            mac_address='Unknown'

            # Extract the IP addresses and MAC addresses
            # the loop loops through the XML elements, and each has only 1 tag so we check for 1 at a time
            for address in host.findall('address'):
                addr_type=address.get('addrtype')
                if addr_type=='ipv4':
                    ip_address=address.get('addr')
                elif addr_type=='mac':
                    mac_address=address.get('addr')

            # If no IP address was found, skip this host
            if ip_address is None:
                continue

            # Extract the open ports and their service information
            print(f"Scanning host {ip_address} with MAC {mac_address}...")
            open_ports=[]
            # find the ports node in the XML tree for this host
            ports_node=host.find('ports')

            if ports_node is not None:
                # for each port node, check if the state is 'open' and if so, extract the port number and service information
                for port in ports_node.findall('port'):
                    if port.find('state').get('state')=='open':
                         port_id=int(port.get('portid'))

                         service_node=port.find('service')
                         service_name='Unknown'
                         banner=''
                         cpe_list=[]

                         #if service node is found, extract the service name and version, otherwise set them to 'Unknown'
                         if service_node is not None:
                             service_name=service_node.get('name','Unknown').upper()
                             product=service_node.get('product','')
                             version=service_node.get('version','')
                             extra_info=service_node.get('extrainfo','')

                             #Extracting the CPE (Common Platform Enumeration) information if available 
                             # to easily fingerprint the device in the Database
                             for cpe in service_node.findall('cpe'):
                                 if cpe.text:
                                     cpe_list.append(cpe.text)

                             #constructing the banner string by concatenating the product, version
                             banner_parts=[product,version]
                             if extra_info:
                                 banner_parts.append(extra_info)

                             banner=' '.join(filter(None,banner_parts)).strip()

                         else:
                                service_name='Unknown'
                                banner='Unknown'
                                cpe_list=[]

                         open_ports.append({
                                 "port":port_id,
                                "service":service_name,
                                 "banner":banner if banner else service_name,
                                 "cpe": cpe_list
                             })
            if not open_ports:
                continue

            # Append the discovered device information to the list
            print(f"Discovered device: IP={ip_address}, MAC={mac_address}, Open Ports={len(open_ports)}")
            discovered_devices.append({
                "ip":ip_address,
                "mac":mac_address,
                "open_ports":open_ports
            })

        response_schema["discovered_devices"]=discovered_devices
        return json.dumps(response_schema,indent=2)


    except ET.ParseError as e:
        response_schema["status"]="failed"
        response_schema["error"]=f"XML Parsing error: {str(e)}"
        return json.dumps(response_schema,indent=2)
    
    except subprocess.SubprocessError as e:
            response_schema["status"]="failed"
            response_schema["error"]=f"Subprocess scanner error: {str(e)}"
            return json.dumps(response_schema,indent=2)


    except Exception as e:
        response_schema["status"]="failed"
        response_schema["error"]=f"Unexpected scanner error: {str(e)}"
        return json.dumps(response_schema,indent=2)

if __name__=="__main__":
    #executing the scan
    result=run_network_scan("192.168.1.0/24") #ip addresses to target for scanning
    print(result)