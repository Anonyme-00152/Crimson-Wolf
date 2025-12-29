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


from Plugins.Utils import *
from Plugins.Config import *

try:
    import os
    import json
    import webbrowser
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    import requests
    import folium
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
    import tkinter as tk
    from tkinter import filedialog
    import threading
    import base64
    from io import BytesIO
except Exception as e:
    MissingModule(e)

def extract_gps_coordinates(exif_data):
    """Extract GPS coordinates from EXIF data"""
    if not exif_data or 34853 not in exif_data:
        return None
    
    gps_info = exif_data[34853]
    gps_data = {}
    
    for tag in gps_info.keys():
        tag_name = GPSTAGS.get(tag, tag)
        gps_data[tag_name] = gps_info[tag]
    
    def convert_to_degrees(value):
        """Convert GPS coordinates to decimal degrees"""
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)
    
    try:
        lat = convert_to_degrees(gps_data.get('GPSLatitude', (0, 0, 0)))
        lat_ref = gps_data.get('GPSLatitudeRef', 'N')
        if lat_ref == 'S':
            lat = -lat
        
        lon = convert_to_degrees(gps_data.get('GPSLongitude', (0, 0, 0)))
        lon_ref = gps_data.get('GPSLongitudeRef', 'E')
        if lon_ref == 'W':
            lon = -lon
        
        altitude = gps_data.get('GPSAltitude', 0)
        if isinstance(altitude, tuple):
            altitude = altitude[0] / altitude[1]
        
        return {
            'latitude': lat,
            'longitude': lon,
            'altitude': altitude,
            'lat_ref': lat_ref,
            'lon_ref': lon_ref,
            'raw': gps_data
        }
    except:
        return None

def get_address_from_coords(lat, lon):
    """Reverse geocode coordinates to address"""
    try:
        geolocator = Nominatim(user_agent="exif_extractor")
        location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
        return location.address if location else "Address not found"
    except GeocoderTimedOut:
        return "Geocoding timeout"
    except:
        return "Geocoding failed"

def create_map(lat, lon, filename):
    """Create interactive map with location marker"""
    try:
        # Create map centered on coordinates
        m = folium.Map(location=[lat, lon], zoom_start=15)
        
        # Add marker
        folium.Marker(
            [lat, lon],
            popup=f"Image Location: {filename}",
            tooltip="Click for details",
            icon=folium.Icon(color='red', icon='camera', prefix='fa')
        ).add_to(m)
        
        # Add circle for accuracy
        folium.Circle(
            location=[lat, lon],
            radius=50,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.2
        ).add_to(m)
        
        # Save map
        map_file = os.path.join(os.path.dirname(filename), f"map_{os.path.basename(filename).split('.')[0]}.html")
        m.save(map_file)
        return map_file
    except:
        return None

def analyze_metadata(exif_data):
    """Analyze metadata for privacy concerns"""
    warnings = []
    sensitive_tags = [
        'GPSInfo', 'GPSLatitude', 'GPSLongitude', 'GPSAltitude',
        'DateTimeOriginal', 'DateTimeDigitized', 'DateTime',
        'Make', 'Model', 'SerialNumber', 'LensSerialNumber',
        'Artist', 'Copyright', 'Software', 'HostComputer'
    ]
    
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name in sensitive_tags and value:
            warnings.append({
                'tag': tag_name,
                'value': str(value)[:100] + "..." if len(str(value)) > 100 else str(value),
                'risk': 'HIGH' if 'GPS' in tag_name or 'Serial' in tag_name else 'MEDIUM'
            })
    
    return warnings

def remove_metadata(image_path, output_path):
    """Remove EXIF metadata from image"""
    try:
        image = Image.open(image_path)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(output_path)
        return True
    except:
        return False

def main():
    Clear()
    Title("EXIF Extractor")
    
    print(f"""
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
                     {red}▓█████ ██▒   █▓ ██▓███   ██▓    
                     {red}▓█   ▀▓██░   █▒▓██░  ██▒▓██▒    
                     {red}▒███   ▓██  █▒░▓██░ ██▓▒▒██░    
                     {red}▒▓█  ▄  ▒██ █░░▒██▄█▓▒ ▒▒██░    
                     {red}░▒████▒  ▒▀█░  ▒██▒ ░  ░░██████▒
                     {red}░░ ▒░ ░  ░ ▐░  ▒▓▒░ ░  ░░ ▒░▓  ░
                     {red} ░ ░  ░  ░ ░░  ░▒ ░     ░ ░ ▒  ░
                     {red}   ░       ░░  ░░         ░ ░   
                     {red}   ░  ░     ░               ░  ░
                     {red}          ░                     
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    {INFO} Tool:{red} Image Metadata & EXIF Extractor
    {INFO} Author:{red} v4lkyr_
    {INFO} Description:{red} Extract, analyze and remove image metadata
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    """)
    
    print(f"{INFO} Options:{red}")
    print(f"  1. Extract metadata from single image")
    print(f"  2. Batch extract from folder")
    print(f"  3. Remove metadata from image")
    print(f"  4. Analyze for privacy risks")
    print(f"  5. Back to main menu{reset}")
    
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip()
    
    if choice == "1":
        extract_single_image()
    elif choice == "2":
        batch_extract()
    elif choice == "3":
        remove_metadata_tool()
    elif choice == "4":
        analyze_privacy()
    else:
        Reset()

def extract_single_image():
    """Extract metadata from single image"""
    Clear()
    Title("EXIF Extractor - Single Image")
    
    print(f"\n{INFO} Select an image file{reset}")
    
    # File dialog
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
    )
    
    if not file_path:
        print(f"{ERROR} No file selected{reset}")
        Continue()
        Reset()
    
    print(f"{SUCCESS} Selected:{red} {file_path}{reset}")
    print(f"{LOADING} Extracting metadata...{reset}")
    
    try:
        # Open and extract EXIF
        image = Image.open(file_path)
        exif_data = image._getexif()
        
        if not exif_data:
            print(f"{ERROR} No EXIF metadata found{reset}")
            Continue()
            Reset()
        
        # Extract GPS data
        gps_data = extract_gps_coordinates(exif_data)
        
        # Display basic info
        print(f"\n{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
        print(f"{red}                     IMAGE INFORMATION{white}")
        print(f"{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
        
        print(f"{INFO} File:{red} {os.path.basename(file_path)}")
        print(f"{INFO} Size:{red} {os.path.getsize(file_path) / 1024:.2f} KB")
        print(f"{INFO} Dimensions:{red} {image.size[0]}x{image.size[1]}")
        print(f"{INFO} Format:{red} {image.format}")
        print(f"{INFO} Mode:{red} {image.mode}{reset}")
        
        # Display EXIF metadata
        print(f"\n{green}✓ EXIF METADATA:{reset}")
        print(f"{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
        
        categories = {
            'Camera Info': ['Make', 'Model', 'Software', 'LensModel', 'LensMake'],
            'Date/Time': ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized'],
            'Camera Settings': ['ExposureTime', 'FNumber', 'ISOSpeedRatings', 'FocalLength', 
                               'ExposureProgram', 'MeteringMode', 'Flash', 'WhiteBalance'],
            'Image Info': ['ImageWidth', 'ImageLength', 'Orientation', 'ResolutionUnit',
                          'XResolution', 'YResolution', 'ColorSpace'],
            'GPS Info': ['GPSInfo', 'GPSLatitude', 'GPSLongitude', 'GPSAltitude'],
            'Other': ['Artist', 'Copyright', 'UserComment', 'XPKeywords']
        }
        
        for category, tags in categories.items():
            category_found = False
            category_data = []
            
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name in tags and value:
                    category_found = True
                    # Format value for display
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = str(value)[:50]
                    
                    value_str = str(value)
                    if len(value_str) > 50:
                        value_str = value_str[:47] + "..."
                    
                    category_data.append(f"  {PREFIX}+{SUFFIX} {tag_name}: {red}{value_str}{reset}")
            
            if category_found:
                print(f"\n{white}▶ {category}:{reset}")
                for line in category_data:
                    print(line)
        
        # GPS Analysis
        if gps_data:
            print(f"\n{red}⚠ GPS DATA FOUND:{reset}")
            print(f"  {PREFIX}!{SUFFIX} Latitude: {red}{gps_data['latitude']:.6f}° {gps_data['lat_ref']}{reset}")
            print(f"  {PREFIX}!{SUFFIX} Longitude: {red}{gps_data['longitude']:.6f}° {gps_data['lon_ref']}{reset}")
            print(f"  {PREFIX}!{SUFFIX} Altitude: {red}{gps_data['altitude']:.1f} meters{reset}")
            
            # Get address
            print(f"{LOADING} Reverse geocoding...{reset}")
            address = get_address_from_coords(gps_data['latitude'], gps_data['longitude'])
            print(f"  {PREFIX}!{SUFFIX} Approximate Address: {red}{address}{reset}")
            
            # Create map option
            create_map_choice = input(f"\n{INPUT} Create interactive map? {YESORNO} {red}->{reset} ").lower()
            if create_map_choice == 'y':
                print(f"{LOADING} Creating map...{reset}")
                map_file = create_map(gps_data['latitude'], gps_data['longitude'], file_path)
                if map_file:
                    print(f"{SUCCESS} Map saved:{red} {map_file}{reset}")
                    
                    open_map = input(f"{INPUT} Open map in browser? {YESORNO} {red}->{reset} ").lower()
                    if open_map == 'y':
                        webbrowser.open(f"file://{os.path.abspath(map_file)}")
        
        # Save results
        save = input(f"\n{INPUT} Save metadata to file? {YESORNO} {red}->{reset} ").lower()
        if save == 'y':
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results_dir = os.path.join(tool_path, 'Programs', 'Results', 'EXIF')
            os.makedirs(results_dir, exist_ok=True)
            
            filename_base = os.path.basename(file_path).split('.')[0]
            json_file = os.path.join(results_dir, f"exif_{filename_base}_{timestamp}.json")
            txt_file = os.path.join(results_dir, f"exif_{filename_base}_{timestamp}.txt")
            
            # Save as JSON
            exif_dict = {}
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        value = str(value)
                exif_dict[tag_name] = value
            
            if gps_data:
                exif_dict['GPS_Data'] = gps_data
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(exif_dict, f, indent=2, default=str)
            
            # Save as text
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"EXIF Metadata Extraction Report\n")
                f.write(f"File: {file_path}\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    f.write(f"{tag_name}: {value}\n")
                
                if gps_data:
                    f.write("\n" + "="*60 + "\n")
                    f.write("GPS DATA:\n")
                    for key, value in gps_data.items():
                        f.write(f"{key}: {value}\n")
            
            print(f"{SUCCESS} Metadata saved to:{red}")
            print(f"  JSON: Programs/Results/EXIF/{os.path.basename(json_file)}")
            print(f"  Text: Programs/Results/EXIF/{os.path.basename(txt_file)}{reset}")
    
    except Exception as e:
        print(f"{ERROR} Error: {red}{str(e)}{reset}")
    
    Continue()
    Reset()

def batch_extract():
    """Batch extract metadata from folder"""
    Clear()
    Title("EXIF Extractor - Batch Mode")
    
    print(f"\n{INFO} Select folder with images{reset}")
    
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    folder_path = filedialog.askdirectory(title="Select Folder with Images")
    
    if not folder_path or not os.path.exists(folder_path):
        print(f"{ERROR} Invalid folder{reset}")
        Continue()
        Reset()
    
    # Get image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']
    image_files = []
    
    for root_dir, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root_dir, file))
    
    if not image_files:
        print(f"{ERROR} No image files found in folder{reset}")
        Continue()
        Reset()
    
    print(f"{SUCCESS} Found:{red} {len(image_files)} image files{reset}")
    print(f"{LOADING} Starting batch extraction...{reset}")
    
    results = []
    files_with_gps = 0
    files_without_exif = 0
    
    for i, image_path in enumerate(image_files):
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            
            if exif_data:
                gps_data = extract_gps_coordinates(exif_data)
                
                result = {
                    'filename': os.path.basename(image_path),
                    'path': image_path,
                    'has_exif': True,
                    'has_gps': gps_data is not None,
                    'gps_data': gps_data,
                    'exif_count': len(exif_data)
                }
                
                if gps_data:
                    files_with_gps += 1
                
                results.append(result)
                
                # Progress
                if (i + 1) % 10 == 0 or (i + 1) == len(image_files):
                    print(f"{LOADING} Processed: {red}{i + 1}/{len(image_files)}{white} files{reset}", end="\r")
            else:
                files_without_exif += 1
                results.append({
                    'filename': os.path.basename(image_path),
                    'path': image_path,
                    'has_exif': False,
                    'has_gps': False
                })
        
        except:
            results.append({
                'filename': os.path.basename(image_path),
                'path': image_path,
                'error': 'Could not read file'
            })
    
    print(f"\n{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
    print(f"{red}                    BATCH EXTRACTION RESULTS{white}")
    print(f"{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
    
    print(f"{INFO} Statistics:{red}")
    print(f"  • Total files: {len(image_files)}")
    print(f"  • With EXIF data: {len(results) - files_without_exif}")
    print(f"  • Without EXIF: {files_without_exif}")
    print(f"  • With GPS coordinates: {files_with_gps}")
    print(f"  • Failed to read: {len([r for r in results if 'error' in r])}{reset}")
    
    if files_with_gps > 0:
        print(f"\n{red}⚠ FILES WITH GPS DATA:{reset}")
        gps_files = [r for r in results if r.get('has_gps')]
        for i, result in enumerate(gps_files[:5]):
            print(f"  {PREFIX}!{SUFFIX} {result['filename']}")
            if result['gps_data']:
                print(f"      Lat: {result['gps_data']['latitude']:.6f}, Lon: {result['gps_data']['longitude']:.6f}")
        
        if len(gps_files) > 5:
            print(f"  {red}... and {len(gps_files) - 5} more{reset}")
    
    # Save summary
    save = input(f"\n{INPUT} Save batch results? {YESORNO} {red}->{reset} ").lower()
    if save == 'y':
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(tool_path, 'Programs', 'Results', 'EXIF_Batch')
        os.makedirs(results_dir, exist_ok=True)
        
        csv_file = os.path.join(results_dir, f"batch_exif_{timestamp}.csv")
        summary_file = os.path.join(results_dir, f"batch_summary_{timestamp}.txt")
        
        # Save CSV
        import csv
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Has_EXIF', 'Has_GPS', 'EXIF_Count', 
                           'Latitude', 'Longitude', 'Altitude', 'Path'])
            
            for result in results:
                if result.get('has_exif'):
                    gps = result.get('gps_data', {})
                    writer.writerow([
                        result['filename'],
                        'Yes',
                        'Yes' if result.get('has_gps') else 'No',
                        result.get('exif_count', 0),
                        gps.get('latitude', ''),
                        gps.get('longitude', ''),
                        gps.get('altitude', ''),
                        result['path']
                    ])
                else:
                    writer.writerow([
                        result['filename'],
                        'No',
                        'No',
                        0, '', '', '', result.get('path', '')
                    ])
        
        # Save summary
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Batch EXIF Extraction Summary\n")
            f.write(f"Folder: {folder_path}\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total files: {len(image_files)}\n")
            f.write(f"With EXIF: {len(results) - files_without_exif}\n")
            f.write(f"With GPS: {files_with_gps}\n")
            f.write("="*60 + "\n\n")
            
            f.write("Files with GPS data:\n")
            for result in [r for r in results if r.get('has_gps')]:
                f.write(f"- {result['filename']}\n")
                if result.get('gps_data'):
                    f.write(f"  Latitude: {result['gps_data']['latitude']}\n")
                    f.write(f"  Longitude: {result['gps_data']['longitude']}\n")
                    f.write(f"  Altitude: {result['gps_data']['altitude']}\n\n")
        
        print(f"{SUCCESS} Results saved to:{red}")
        print(f"  CSV: Programs/Results/EXIF_Batch/{os.path.basename(csv_file)}")
        print(f"  Summary: Programs/Results/EXIF_Batch/{os.path.basename(summary_file)}{reset}")
    
    Continue()
    Reset()

def remove_metadata_tool():
    """Remove metadata from images"""
    Clear()
    Title("EXIF Remover")
    
    print(f"\n{INFO} Select action:{red}")
    print(f"  1. Remove metadata from single image")
    print(f"  2. Batch remove metadata from folder")
    print(f"  3. Back{reset}")
    
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip()
    
    if choice == "1":
        # Single image removal
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(
            title="Select Image to Clean",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.tiff *.tif *.bmp")]
        )
        
        if file_path:
            output_path = filedialog.asksaveasfilename(
                title="Save Cleaned Image As",
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All files", "*.*")]
            )
            
            if output_path:
                print(f"{LOADING} Removing metadata...{reset}")
                success = remove_metadata(file_path, output_path)
                
                if success:
                    print(f"{SUCCESS} Metadata removed:{red} {output_path}{reset}")
                    
                    # Verify removal
                    try:
                        image = Image.open(output_path)
                        if not image._getexif():
                            print(f"{SUCCESS} Verification: No EXIF data found{reset}")
                        else:
                            print(f"{ERROR} Verification: EXIF data still present{reset}")
                    except:
                        print(f"{INFO} Could not verify removal{reset}")
                else:
                    print(f"{ERROR} Failed to remove metadata{reset}")
    
    elif choice == "2":
        # Batch removal
        folder_path = filedialog.askdirectory(title="Select Folder with Images")
        
        if folder_path:
            output_folder = filedialog.askdirectory(title="Select Output Folder")
            
            if output_folder:
                image_extensions = ['.jpg', '.jpeg', '.png']
                image_files = []
                
                for root_dir, dirs, files in os.walk(folder_path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in image_extensions):
                            image_files.append(os.path.join(root_dir, file))
                
                print(f"{LOADING} Processing {len(image_files)} images...{reset}")
                
                success_count = 0
                for i, image_path in enumerate(image_files):
                    try:
                        filename = os.path.basename(image_path)
                        output_path = os.path.join(output_folder, f"cleaned_{filename}")
                        
                        if remove_metadata(image_path, output_path):
                            success_count += 1
                        
                        if (i + 1) % 10 == 0:
                            print(f"{LOADING} Processed: {red}{i + 1}/{len(image_files)}{reset}", end="\r")
                    
                    except:
                        continue
                
                print(f"\n{SUCCESS} Completed:{red} {success_count}/{len(image_files)} images cleaned{reset}")
    
    Continue()
    Reset()

def analyze_privacy():
    """Analyze images for privacy risks"""
    Clear()
    Title("Privacy Analyzer")
    
    print(f"\n{INFO} This tool analyzes images for sensitive metadata{reset}")
    
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_path = filedialog.askopenfilename(
        title="Select Image to Analyze",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    
    if not file_path:
        Reset()
    
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        
        if not exif_data:
            print(f"{SUCCESS} No EXIF metadata found - Low privacy risk{reset}")
            Continue()
            Reset()
        
        warnings = analyze_metadata(exif_data)
        gps_data = extract_gps_coordinates(exif_data)
        
        print(f"\n{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
        print(f"{red}                   PRIVACY ANALYSIS REPORT{white}")
        print(f"{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
        
        print(f"{INFO} File:{red} {os.path.basename(file_path)}{reset}")
        
        if gps_data:
            print(f"\n{red}⚠⚠⚠ CRITICAL RISK: GPS DATA FOUND{reset}")
            print(f"  {PREFIX}!{SUFFIX} Location can be tracked to exact coordinates")
            print(f"  {PREFIX}!{SUFFIX} Latitude: {red}{gps_data['latitude']:.6f}°{reset}")
            print(f"  {PREFIX}!{SUFFIX} Longitude: {red}{gps_data['longitude']:.6f}°{reset}")
            
            address = get_address_from_coords(gps_data['latitude'], gps_data['longitude'])
            print(f"  {PREFIX}!{SUFFIX} Approximate address: {red}{address}{reset}")
        
        if warnings:
            print(f"\n{yellow}⚠ POTENTIAL PRIVACY ISSUES:{reset}")
            
            high_risk = [w for w in warnings if w['risk'] == 'HIGH']
            medium_risk = [w for w in warnings if w['risk'] == 'MEDIUM']
            
            if high_risk:
                print(f"\n{red}  High Risk:{reset}")
                for warning in high_risk:
                    print(f"    {PREFIX}!{SUFFIX} {warning['tag']}: {red}{warning['value']}{reset}")
            
            if medium_risk:
                print(f"\n{yellow}  Medium Risk:{reset}")
                for warning in medium_risk[:5]:
                    print(f"    {PREFIX}+{SUFFIX} {warning['tag']}: {warning['value']}")
                
                if len(medium_risk) > 5:
                    print(f"    {red}... and {len(medium_risk) - 5} more{reset}")
        
        # Recommendations
        print(f"\n{green}✓ RECOMMENDATIONS:{reset}")
        if gps_data or warnings:
            print(f"  1. Remove metadata before sharing online")
            print(f"  2. Use the 'Remove Metadata' tool in this program")
            print(f"  3. Consider blurring faces/identifying features")
            print(f"  4. Review social media privacy settings")
        else:
            print(f"  1. Image appears safe to share")
            print(f"  2. No sensitive metadata detected")
        
        print(f"\n{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
        
        # Action options
        print(f"\n{INFO} Actions:{red}")
        print(f"  1. Remove metadata now")
        print(f"  2. View all metadata")
        print(f"  3. Save report")
        print(f"  4. Back{reset}")
        
        action = input(f"{INPUT} Choice {red}->{reset} ").strip()
        
        if action == "1":
            output_path = filedialog.asksaveasfilename(
                title="Save Cleaned Image",
                defaultextension=".jpg",
                initialfile=f"cleaned_{os.path.basename(file_path)}"
            )
            
            if output_path:
                if remove_metadata(file_path, output_path):
                    print(f"{SUCCESS} Metadata removed:{red} {output_path}{reset}")
        
        elif action == "2":
            # Show all metadata
            print(f"\n{white}All EXIF Metadata:{reset}")
            print(f"{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
            
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:97] + "..."
                print(f"{tag_name}: {value_str}")
        
        elif action == "3":
            # Save report
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results_dir = os.path.join(tool_path, 'Programs', 'Results', 'Privacy')
            os.makedirs(results_dir, exist_ok=True)
            
            report_file = os.path.join(results_dir, f"privacy_report_{timestamp}.txt")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"Privacy Analysis Report\n")
                f.write(f"File: {file_path}\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"GPS Data Found: {'YES' if gps_data else 'NO'}\n")
                if gps_data:
                    f.write(f"Latitude: {gps_data['latitude']}\n")
                    f.write(f"Longitude: {gps_data['longitude']}\n")
                    f.write(f"Address: {get_address_from_coords(gps_data['latitude'], gps_data['longitude'])}\n\n")
                
                f.write(f"Total warnings: {len(warnings)}\n")
                f.write(f"High risk: {len([w for w in warnings if w['risk'] == 'HIGH'])}\n")
                f.write(f"Medium risk: {len([w for w in warnings if w['risk'] == 'MEDIUM'])}\n\n")
                
                f.write("Detailed warnings:\n")
                for warning in warnings:
                    f.write(f"- [{warning['risk']}] {warning['tag']}: {warning['value']}\n")
                
                f.write("\n" + "="*60 + "\n")
                f.write("RECOMMENDATIONS:\n")
                if gps_data or warnings:
                    f.write("1. Remove metadata before sharing\n")
                    f.write("2. Review what you share online\n")
                    f.write("3. Consider using metadata removal tools\n")
                else:
                    f.write("Image appears safe to share\n")
            
            print(f"{SUCCESS} Report saved to:{red} Programs/Results/Privacy/{os.path.basename(report_file)}{reset}")
    
    except Exception as e:
        print(f"{ERROR} Analysis failed: {red}{str(e)}{reset}")
    
    Continue()
    Reset()

if __name__ == "__main__":
    main()