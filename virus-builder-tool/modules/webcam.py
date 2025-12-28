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

def capture_webcam():
    """Capture webcam image"""
    import cv2
    import base64
    import io
    from PIL import Image
    
    try:
        # Access webcam
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        
        if ret:
            # Convert to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            cam.release()
            
            return {
                "success": True,
                "image_base64": img_str[:100] + "..." if len(img_str) > 100 else img_str,
                "resolution": f"{frame.shape[1]}x{frame.shape[0]}"
            }
        else:
            cam.release()
            return {"success": False, "error": "Could not capture image"}
    except Exception as e:
        return {"success": False, "error": str(e)}
