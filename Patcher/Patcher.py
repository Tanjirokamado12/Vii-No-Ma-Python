import os
import sys
import subprocess
import shutil

print("""
========

Vii No Ma Auto Patcher

========

Auto Patcher is experimental and may not work

When reporting an issue, send the FULL log
INCLUDING all arguments and OS.

And in all cases,Don't use at all Wiilink wads,It will not Work at all and it will Brick the wad
""")

# -------------------------
# Version selection
# -------------------------
version_options = ["v0", "v512", "v770", "v1025"]

print("Select a version:")
for i, v in enumerate(version_options, 1):
    print(f"{i}. {v}")

while True:
    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(version_options):
            break
        print("Input valid number, please.")
    except ValueError:
        print("Input valid number, please.")

selected_version = version_options[choice - 1]
wad_file = f"{selected_version}.wad"

print(f"You selected: {selected_version}")
print(f"Ensure {wad_file} is in the same directory.")

# -------------------------
# IP selection
# -------------------------
ip_choice = input("Use Dolphin (D) or IP (S)? ").strip().lower()

if ip_choice == "d":
    ip_address = "127.0.0.1/"
elif ip_choice == "s":
    ip_address = input("Enter IP: ").strip() + "/"
else:
    print("Invalid choice.")
    sys.exit(1)

input("Press Enter to continue...")

def patch_scene_name(data: bytearray):
    old = b"InputRegionScene"
    new = b"LivingRoomScene"

    if len(new) > len(old):
        raise ValueError("Replacement string is longer than original")

    padded_new = new + b"\x00" * (len(old) - len(new))

    idx = 0
    while True:
        idx = data.find(old, idx)
        if idx == -1:
            break

        data[idx:idx + len(old)] = padded_new
        print("Patched InputRegionScene -> LivingRoomScene")

        idx += len(old)

# -------------------------
# OS check
# -------------------------
if not sys.platform.startswith("win"):
    print("Windows only.")
    sys.exit(1)

root = os.path.abspath(os.path.dirname(__file__))

print("Launching Sharpii...")

wad_path = os.path.join(root, wad_file)
sharpii = os.path.join(root, "Sharpii.exe")

# -------------------------
# Step 1: unpack WAD
# -------------------------
subprocess.run(
    f'"{sharpii}" WAD -u "{wad_path}" temp',
    shell=True,
    check=True
)

# -------------------------
# Step 2: copy lzx
# -------------------------
shutil.copy(
    os.path.join(root, "lzx.exe"),
    os.path.join(root, "temp", "lzx.exe")
)

# -------------------------
# Step 3: decompress app
# -------------------------
subprocess.run(
    "lzx -d 00000001.app 00000001.app",
    cwd=os.path.join(root, "temp"),
    shell=True,
    check=True
)

app_path = os.path.join(root, "temp", "00000001.app")

with open(app_path, "rb") as f:
    data = bytearray(f.read())

# -------------------------
# Scene patch (v770 / v1025 only)
# -------------------------
if selected_version in ["v770", "v1025"]:
    patch_scene_name(data)

# -------------------------
# URL selection (wmp)
# -------------------------
if selected_version == "v770":
    search_url = b"https://a248.e.akamai.net/f/248/81607/7d/wmp1v2.wapp.wii.com/"
elif selected_version == "v1025":
    search_url = b"https://a248.e.akamai.net/f/248/93025/7d/wmp3v2.wapp.wii.com/"
else:
    search_url = b"https://a248.e.akamai.net/f/248/70236/7d/wmp1.wapp.wii.com/"

# -------------------------
# Replace WMP URL
# -------------------------
idx = data.find(search_url)
if idx != -1:
    new_url = f"http://{ip_address}".encode()
    padded = new_url + b"\x00" * (len(search_url) - len(new_url))
    data[idx:idx + len(search_url)] = padded
    print("Modified WMP URL")
else:
    print("WMP URL not found")

# -------------------------
# ECS SHOP PATCH (your request)
# -------------------------
ecs_pattern = b"https://ecs.shop.wii.com/"

idx = 0
while True:
    idx = data.find(ecs_pattern, idx)
    if idx == -1:
        break

    end = idx + len(ecs_pattern)
    while end < len(data) and data[end] not in (0x00, 0x20, 0x0A, 0x0D):
        end += 1

    original = data[idx:end]
    path = original[len(ecs_pattern):].decode(errors="ignore")

    new_url = f"http://{ip_address}{path}".encode()
    replacement = new_url.ljust(len(original), b"\x00")

    data[idx:idx+len(original)] = replacement

    print(f"ECS patched: {path}")

    idx += len(replacement)

# -------------------------
# First.bin replace
# -------------------------
old = b"https://wmp2v3.wapp.wii.com/conf/first.bin"
idx = data.find(old)

if idx != -1:
    new_url = f"http://{ip_address}v1025/first.bin".encode()
    padded = new_url + b"\x00" * (len(old) - len(new_url))
    data[idx:idx+len(old)] = padded
    print("Patched first.bin")
else:
    print("first.bin not found")

# -------------------------
# .img -> .jpg
# -------------------------
data = data.replace(b".img", b".jpg")


# -------------------------
# v0/v512 patch
# -------------------------
if selected_version in ["v0", "v512"]:
    data = data.replace(b"conf/first.bin", b"v512/first.bin")

# -------------------------
# write back
# -------------------------
with open(app_path, "wb") as f:
    f.write(data)

# -------------------------
# recompress
# -------------------------
subprocess.run(
    "lzx -evb 00000001.app 00000001.app",
    cwd=os.path.join(root, "temp"),
    shell=True,
    check=True
)

# -------------------------
# repack WAD
# -------------------------
subprocess.run(
    f"sharpii.exe wad -p temp {selected_version}_patched.wad",
    cwd=root,
    shell=True,
    check=True
)

print("Done.")