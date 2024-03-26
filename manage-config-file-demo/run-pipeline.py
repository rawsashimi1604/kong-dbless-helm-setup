import os
import yaml
import requests
import subprocess
import time

from testcontainers.core.container import DockerContainer

# Constants
DEFAULT_MERGE_SCRIPT_PATH = "./merge_files.sh"
DEFAULT_MERGE_FILE_PATH = "./merged.yaml"
KONG_DECK_FILE_OUTPUT_FORMAT = "yaml"
KONG_DECK_FILE_OUTPUT = "merged.yaml"

# Testcontainers
class DeckContainer(DockerContainer):
    """An instance of Kong deck in a docker container."""

    KONG_DECK_IMAGE = "kong/deck:v1.36.1"

    def __init__(self, command: list, image=KONG_DECK_IMAGE):
        """Create a new instance of Kong Deck."""

        super().__init__(image)
        self.with_volume_mapping(os.getcwd(), '/data', 'rw')
        self.with_command(command)
        self.start()

        logs = self.get_logs()
        for log in logs:
            # Error when running validate
            decoded = log.decode('utf-8').strip()
            if ("Error: building state: " in decoded):
                raise Exception("error when decoding")
            print(log.decode('utf-8').strip())

        

class KongDblessContainer(DockerContainer):
    """An instance of Kong running in DB-less mode in a docker container."""
    
    DEFAULT_IMAGE="kong/kong-gateway:2.8.4.7-alpine"
    

    def __init__(self, image=DEFAULT_IMAGE):
        """Create a new instance of Kong running in DB-less mode."""

        super().__init__(image)
        self.with_name("kong-dbless")
        self.with_env("KONG_DATABASE", "off")
        self.with_env("KONG_PROXY_ACCESS_LOG", "/dev/stdout")
        self.with_env("KONG_ADMIN_ACCESS_LOG", "/dev/stdout")
        self.with_env("KONG_PROXY_ERROR_LOG", "/dev/stderr")
        self.with_env("KONG_ADMIN_ERROR_LOG", "/dev/stderr")
        self.with_env("KONG_ADMIN_LISTEN", "0.0.0.0:8001")
        self.with_env("KONG_ADMIN_GUI_URL", "http://localhost:8002")
        self.with_exposed_ports(8000, 8443, 8001, 8444, 8002, 8445, 8003, 8004)

    def wait_for_ready(self, timeout=60):
        """Wait for Kong Admin API to become responsive."""

        start_time = time.time()
        # Curl the admin api
        url = f"http://{self.get_container_host_ip()}:{self.get_exposed_port('8001')}/"
        while True:
            try:
                print("[*] Waiting for Kong to become ready, testing GET /config")
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print("[*] Kong is ready! GET /config returned 200 OK")
                    break

            except requests.exceptions.RequestException:
                pass  # Ignore network-related errors during startup

            if time.time() - start_time > timeout:
                raise TimeoutError("[*] Timed out waiting for Kong to become ready")
            time.sleep(1)

    def start(self):
        """Start the Kong container"""

        super().start()
        self.wait_for_ready()
        return self
    
    def testAdminConfigRoute(self, config_file=DEFAULT_MERGE_FILE_PATH):
        """Injects Kong configuration from a file."""

        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)

        url = f"http://{self.get_container_host_ip()}:{self.get_exposed_port('8001')}/config"
        response = requests.post(url, json=config_data)
        if response.status_code != 201:
            print("\n[*] Invalid response received:\n" +  response.text + "\n")
            raise Exception("Failed to inject Kong configuration")
        print("\n[*] Valid response received 201:\n" +  response.text + "\n")
        

if __name__ == "__main__":
    print("[*] Starting CI Pipeline\n")
    
    print("[*] Merging configuration files")
    exit_code = subprocess.call(DEFAULT_MERGE_SCRIPT_PATH)
    if exit_code != 0:
        raise Exception("Failed to merge configuration files. Exiting...")
    print("\n[+] Kong declarative file created")
    time.sleep(1)

    print("[*] Validating kong configuration file...")
    exit_code = subprocess.call("./validate_file.sh")
    if exit_code != 0:
        raise Exception("Invalid kong configuration detected. Exiting...")
    print("[*] Kong configuration file is valid\n")
    time.sleep(1)

    print("[*] Starting config file with kong integration test")
    with KongDblessContainer() as kong:
        print("[*] Starting kong container")
        print("[+] Kong container started")
        print("[*] Running integration test")
        kong.testAdminConfigRoute()
        print("[*] Integration test finished\n")
        print("[*] CI Pipeline finished\n")
    
    # end 