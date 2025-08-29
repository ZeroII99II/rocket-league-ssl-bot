#!/usr/bin/env python3
"""
Download RLViser executable
"""

import urllib.request
import os
import zipfile
import shutil

def download_rlviser():
    """Download pre-built RLViser executable"""
    try:
        print("🔽 Downloading RLViser executable...")
        
        # RLViser release URL (latest release)
        url = "https://github.com/VirxEC/rlviser/releases/latest/download/rlviser-windows.zip"
        
        # Download the file
        print("   📥 Downloading from GitHub...")
        urllib.request.urlretrieve(url, "rlviser.zip")
        
        # Extract the zip
        print("   📦 Extracting...")
        with zipfile.ZipFile("rlviser.zip", 'r') as zip_ref:
            zip_ref.extractall("rlviser_extracted")
        
        # Find the executable
        for root, dirs, files in os.walk("rlviser_extracted"):
            for file in files:
                if file.endswith(".exe"):
                    exe_path = os.path.join(root, file)
                    print(f"   ✅ Found executable: {exe_path}")
                    
                    # Copy to main directory
                    shutil.copy2(exe_path, "rlviser.exe")
                    print("   ✅ Copied rlviser.exe to main directory")
                    
                    # Clean up
                    shutil.rmtree("rlviser_extracted")
                    os.remove("rlviser.zip")
                    
                    return True
        
        print("   ❌ No executable found in download")
        return False
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("   💡 Trying alternative approach...")
        return False

if __name__ == "__main__":
    print("🚀 RLViser Downloader")
    print("=" * 50)
    download_rlviser()

