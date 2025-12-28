
def show_fake_error():
    """Show fake error message"""
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            "This application requires .NET Framework 4.8.\nPlease install it and try again.",
            "Runtime Error",
            0x10
        )
        return True
    except:
        return False
