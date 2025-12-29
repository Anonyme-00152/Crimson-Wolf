
def check_vm():
    """Check if running in virtual machine"""
    import platform
    import subprocess
    
    vm_indicators = [
        "vmware", "virtualbox", "qemu", "xen", "vbox", "hyper-v",
        "vmx", "vmic", "hv", "virtual", "innotek", "parallels"
    ]
    
    # Check system info
    system_info = str(platform.uname()).lower()
    
    # Check processes
    try:
        processes = subprocess.check_output("tasklist", shell=True).decode().lower()
    except:
        processes = ""
    
    # Check services
    try:
        services = subprocess.check_output("sc query", shell=True).decode().lower()
    except:
        services = ""
    
    # Combine all checks
    all_checks = system_info + processes + services
    
    for indicator in vm_indicators:
        if indicator in all_checks:
            return True
    
    return False
