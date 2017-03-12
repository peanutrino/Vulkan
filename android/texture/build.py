import os
import shutil
import subprocess
import sys
import glob

APK_NAME = "vulkanTexture"
SHADER_DIR = "texture"
ASSETS_TEXTURES = ["metalplate01_bc2_unorm.ktx", "metalplate01_astc_8x8_unorm.ktx", "metalplate01_etc2_unorm.ktx"]

if subprocess.call("ndk-build", shell=True) == 0:   
    print("Build successful")

    # Assets
    if not os.path.exists("./assets"):
        os.makedirs("./assets")  

    # Shaders    
    # Base
    if not os.path.exists("./assets/shaders/base"):
        os.makedirs("./assets/shaders/base")           
    for file in glob.glob("../../data/shaders/base/*.spv"):
        shutil.copy(file, "./assets/shaders/base")    
    # Sample
    if not os.path.exists("./assets/shaders/%s" % SHADER_DIR):
        os.makedirs("./assets/shaders/%s" % SHADER_DIR)
    for file in glob.glob("../../data/shaders/%s/*.spv" %SHADER_DIR):
        shutil.copy(file, "./assets/shaders/%s" % SHADER_DIR)    
    # Textures
    if not os.path.exists("./assets/textures"):
        os.makedirs("./assets/textures")           
    for file in ASSETS_TEXTURES:
        shutil.copy("../../data/textures/%s" % file, "./assets/textures")        

    # Icon
    if not os.path.exists("./res/drawable"):
        os.makedirs("./res/drawable")         
    shutil.copy("../../android/images/icon.png", "./res/drawable")      

    if subprocess.call("ant debug -Dout.final.file=%s.apk" % APK_NAME, shell=True) == 0:
        if len(sys.argv) > 1:
            if sys.argv[1] == "-deploy":
                if subprocess.call("adb install -r %s.apk" % APK_NAME, shell=True) != 0:
                    print("Could not deploy to device!")
    else:
        print("Error during build process!")
else:
    print("Error building project!")