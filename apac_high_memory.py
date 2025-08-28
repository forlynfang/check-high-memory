#!usr/bin/python3

# This script is to check the memory of Cisco switches, to make sure it is less than 80%
# The output should be a table of switch name, memory percentage for each switch unit
# Usage: python3 apac_high_memory.py --testbed apac_tb.yaml

import logging
import jinja2
import json
from pyats import aetest
from genie.testbed import load
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#TODO: Get the logger for script
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#TODO: Connect to device
class Common_setup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_device(self, testbed):
        for device_name, device in testbed.devices.items():
            log.info(f"Connecting to {device_name}")
            device.connect()
            # Store device_name as variable "device_name", to use in other test cases
            self.parent.parameters['device_name'] = device_name

#TODO: Parse the cli "show platform software status control-processor brief", and write output to a text file to double-check
class Check_memory(aetest.Testcase):
    @aetest.test
    def show_platform_memory(self, testbed):
        self.platform_memory = {}
        for device_name, device in testbed.devices.items():
            log.info(f"{device_name} connected status: {device.connected}")
            log.info(f"Running commnd 'show platform software status control-processor brief' on {device_name}")
            # Add the parse result as the value of key "device_name"
            self.platform_memory[device_name] = device.parse("show platform software status control-processor brief")
        # Display result to console
        log.info(self.platform_memory)
        # Store the platform_memory as variable "platform_memory", to use in other test cases
        self.parent.parameters['platform_memory'] = self.platform_memory
        # Output the result of command to a text file

#TODO: Confirm the memory is less than 80%, and display the memory as a table of switch name, switch unit, memory percentage
class Memory_higher_than_80(aetest.Testcase):
    @aetest.test
    def memory_check(self):
        platform_memory = self.parent.parameters.get('platform_memory', {})
        memory_status = [] 
        for device, info in platform_memory.items():
            for switch_unit, unit_info in info['slot'].items():
                log.info(f"Found switch: {switch_unit}")
                used_memory = unit_info['memory']['used_percentage']

                if int(used_memory) > 80:
                    log.info(f"Memory test of {device} is FAILED ***")
                    teams_webhook_url = "https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c/V2-0LzN76qekmVrAPO1b9pX-4MwxVsHKo7lbMnV_iHFb81"
                    message = {
                    "text": f"WARNING: Memory usage of {device.upper()} is {used_memory}%, which exceeds the threshold of 80%."
                    }
                    try:
                        teams_response = requests.post(
                        teams_webhook_url,
                        json=message,
                        headers={"Content-Type": "application/json"}
                        )
                        teams_response.raise_for_status()
                        print(f"Alert sent to MS Teams for {device}.\n")
                    except Exception as e:
                        print(f"Failed to send alert to MS Teams for {device}: {e}")
      
#TODO: Disconnect from device
class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_device(self, testbed):
        for device_name, device in testbed.devices.items():
            log.info(f"Disconnecting from {device_name}")
            device.disconnect()

if __name__ == ("__main__"):
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=loader.load)
    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
