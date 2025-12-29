# ============================================================
#  Author      : Anonyme-001
#  Project     : Multi-Tool (Educational Purpose Only)
#  Year        : 2025
#
#  DISCLAIMER:
#  This code is provided for EDUCATIONAL PURPOSES ONLY.
#  It is intended to help understand programming, security
#  concepts, and defensive techniques.
#
#  ❌ Any malicious use is strictly prohibited.
#  ❌ Do NOT modify this code to perform illegal actions.
#  ❌ The author is NOT responsible for any misuse.
#
#  By using this code, you agree to use it responsibly
#  and within legal boundaries.
#
#  Copyright (c) 2025 Anonyme-001
#  See LICENSE file for details.
# ============================================================

def take_screenshot():
    """Take screenshot"""
    import io
    import base64
    from PIL import ImageGrab
    
    try:
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Convert to base64
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "success": True,
            "image_base64": img_str[:100] + "..." if len(img_str) > 100 else img_str,
            "size": f"{screenshot.size[0]}x{screenshot.size[1]}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
