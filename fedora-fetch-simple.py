#!/usr/bin/env python3
"""
Semplice script per testare la velocità dei mirror Fedora
e configurare automaticamente quelli più veloci.

Questo è uno script dimostrativo per la funzionalità fetch
di nala-fedora.
"""

import subprocess
import time
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError


FEDORA_MIRRORS = [
    "http://download.fedoraproject.org/pub/fedora/linux/",
    "https://mirror.karneval.cz/pub/linux/fedora/linux/",
    "https://ftp.halifax.rwth-aachen.de/fedora/linux/",
    "https://mirror.23m.com/fedora/linux/",
    "https://fedora.ip-connect.info/",
    "https://mirror.init7.net/fedora/",
    "https://mirror.netcologne.de/fedora/linux/",
    "https://ftp.fau.de/fedora/linux/",
]


def test_mirror_speed(mirror_url, test_file="releases/40/Everything/x86_64/os/repodata/repomd.xml"):
    """Test the speed of a mirror by downloading a small file."""
    try:
        full_url = f"{mirror_url.rstrip('/')}/{test_file}"
        print(f"Testing {urlparse(mirror_url).netloc}...", end=" ")
        
        start_time = time.time()
        with urlopen(full_url, timeout=10) as response:
            _ = response.read(1024)  # Read first 1KB
        end_time = time.time()
        
        speed = 1024 / (end_time - start_time)  # bytes per second
        print(f"{speed:.0f} B/s")
        return mirror_url, speed
        
    except (URLError, OSError, Exception) as e:
        print(f"Failed - {e}")
        return mirror_url, 0


def get_current_fedora_version():
    """Get the current Fedora version."""
    try:
        with open("/etc/fedora-release", "r") as f:
            content = f.read()
            # Extract version number
            import re
            match = re.search(r"Fedora.*?(\d+)", content)
            if match:
                return match.group(1)
    except:
        pass
    
    # Fallback - try to detect from dnf
    try:
        result = subprocess.run(
            ["rpm", "-q", "--queryformat", "%{VERSION}", "fedora-release"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except:
        return "40"  # Default fallback


def create_repo_file(mirrors, fedora_version):
    """Create a .repo file with the fastest mirrors."""
    repo_content = f"""# Nala-Fedora Fast Mirrors
# Generated automatically

[nala-fedora-fast]
name=Fedora $releasever - Fast Mirrors
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-$releasever&arch=$basearch
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=https://getfedora.org/static/fedora.gpg
skip_if_unavailable=False

[nala-fedora-updates-fast]
name=Fedora $releasever - Updates - Fast Mirrors  
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-released-f$releasever&arch=$basearch
enabled=1
countme=1
repo_gpgcheck=0
type=rpm
gpgcheck=1
metadata_expire=6h
gpgkey=https://getfedora.org/static/fedora.gpg
skip_if_unavailable=False
"""
    
    return repo_content


def main():
	"""Main function."""
	# Force English output
	import os
	os.environ["LANG"] = "en_US.UTF-8"
	os.environ["LC_ALL"] = "en_US.UTF-8"
	
	print("🔍 Nala-Fedora Mirror Speed Test")
	print("=" * 40)
	
	# Get Fedora version
	fedora_version = get_current_fedora_version()
	print(f"Detected Fedora version: {fedora_version}")
	print()
	
	# Test mirrors
	print("Testing mirror speeds...")
	results = []
	
	for mirror in FEDORA_MIRRORS:
		result = test_mirror_speed(mirror)
		if result[1] > 0:
			results.append(result)
	
	if not results:
		print("❌ No working mirrors found!")
		return 1
	
	# Sort by speed (fastest first)
	results.sort(key=lambda x: x[1], reverse=True)
	
	print("\n📊 Results (fastest first):")
	print("-" * 40)
	for i, (mirror, speed) in enumerate(results[:5], 1):
		domain = urlparse(mirror).netloc
		print(f"{i}. {domain} - {speed:.0f} B/s")
	
	# Ask user if they want to create repo file
	print(f"\nFound {len(results)} working mirrors.")
	
	try:
		response = input("Create optimized repo file? [y/N]: ").lower()
		if response.startswith('y'):
			# Use top 3 fastest mirrors
			top_mirrors = results[:3]
			repo_content = create_repo_file([m[0] for m in top_mirrors], fedora_version)
			
			repo_file = "/etc/yum.repos.d/nala-fedora-fast.repo"
			with open(repo_file, "w") as f:
				f.write(repo_content)
			
			print(f"✅ Created {repo_file}")
			print("Run 'sudo dnf makecache' to update metadata")
		else:
			print("Repo file not created")
	
	except KeyboardInterrupt:
		print("\n⏹️  Cancelled by user")
		return 1
	
	return 0


if __name__ == "__main__":
    exit(main())