class CodexVirusScanner:
    def scan_module(self, module_content):
        # Simulate detection logic
        if "malicious" in module_content.lower() or "payload" in module_content.lower():
            print("Quarantine initiated. Module isolated.")
            print("Custodian Alert: Threat detected and contained.")
        else:
            print("Module clean. No threats detected.")

# Example usage:
if __name__ == "__main__":
    scanner = CodexVirusScanner()
    scanner.scan_module("malicious payload in finance capsule")
