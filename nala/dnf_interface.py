#                 __
#    ____ _____  |  | _____
#   /    \__  \ |  | \__  \
#  |   |  \/ __ \|  |__/ __ \_
#  |___|  (____  /____(____  /
#       \/     \/          \/
#
# Copyright (C) 2021, 2022 Blake Lee
# Adapted for Fedora/DNF by Gabriele
#
# This file is part of nala-fedora
#
# nala-fedora is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nala-fedora is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with nala-fedora.  If not, see <https://www.gnu.org/licenses/>.
"""Interface module for DNF to replace python-apt functionality."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class DNFConfig:
	"""DNF configuration helper to mimic apt_pkg.config functionality."""

	@staticmethod
	def find_dir(key: str, default: str = "") -> str:
		"""Find DNF directory configuration."""
		# Map APT directories to DNF equivalents
		dir_mapping = {
			"Dir::Cache": "/var/cache/dnf",
			"Dir::Etc": "/etc/dnf",
			"Dir::State::Lists": "/var/cache/dnf",
			"Dir::State::status": "/var/lib/rpm/Packages",
		}
		return dir_mapping.get(key, default)

	@staticmethod
	def find_file(key: str) -> Optional[str]:
		"""Find DNF file configuration."""
		file_mapping = {
			"Dir::Cache::Archives": "/var/cache/dnf/packages",
			"Dir::Cache::pkgcache": "/var/cache/dnf/metadata",
			"Dir::Cache::srcpkgcache": "/var/cache/dnf/metadata",
			"Dir::Etc::sourcelist": "/etc/yum.repos.d",
			"Dir::Etc::sourceparts": "/etc/yum.repos.d",
		}
		return file_mapping.get(key)


class DNFPackage:
	"""DNF package wrapper to mimic python-apt Package functionality."""

	def __init__(self, package_data: Dict[str, Any]):
		"""Initialize DNF package from dnf json output."""
		self.data = package_data
		self.name = package_data.get("name", "")
		self.version = package_data.get("version", "")
		self.release = package_data.get("release", "")
		self.arch = package_data.get("arch", "")
		self.summary = package_data.get("summary", "")
		self.description = package_data.get("description", "")
		self.size = package_data.get("size", 0)
		self.repo = package_data.get("repo", "")

	@property
	def fullname(self) -> str:
		"""Get full package name with version."""
		return f"{self.name}-{self.version}-{self.release}.{self.arch}"

	@property
	def installed(self) -> bool:
		"""Check if package is installed."""
		try:
			result = subprocess.run(
				["rpm", "-q", self.name],
				capture_output=True,
				text=True,
				check=False
			)
			return result.returncode == 0
		except Exception:
			return False

	@property
	def candidate(self) -> "DNFPackage":
		"""Get candidate package (latest available)."""
		return self

	@property
	def installed_version(self) -> Optional[str]:
		"""Get installed version."""
		if not self.installed:
			return None
		try:
			result = subprocess.run(
				["rpm", "-q", "--queryformat", "%{VERSION}-%{RELEASE}", self.name],
				capture_output=True,
				text=True,
				check=True
			)
			return result.stdout.strip()
		except Exception:
			return None


class DNFCache:
	"""DNF cache wrapper to mimic python-apt Cache functionality."""

	def __init__(self):
		"""Initialize DNF cache."""
		self._packages: Dict[str, DNFPackage] = {}
		self._loaded = False

	def open(self, progress=None) -> None:
		"""Open and load the DNF cache."""
		self.update()

	def update(self, progress=None) -> bool:
		"""Update the DNF cache."""
		try:
			# Update metadata
			subprocess.run(
				["dnf", "makecache", "--refresh"],
				capture_output=True,
				check=True
			)
			self._load_packages()
			self._loaded = True
			return True
		except subprocess.CalledProcessError:
			return False

	def _load_packages(self) -> None:
		"""Load packages from DNF."""
		try:
			# Get available packages
			result = subprocess.run(
				["dnf", "repoquery", "--available", "--json"],
				capture_output=True,
				text=True,
				check=True
			)
			
			available_data = json.loads(result.stdout)
			for pkg_data in available_data:
				pkg = DNFPackage(pkg_data)
				self._packages[pkg.name] = pkg

			# Get installed packages
			result = subprocess.run(
				["dnf", "repoquery", "--installed", "--json"],
				capture_output=True,
				text=True,
				check=True
			)
			
			installed_data = json.loads(result.stdout)
			for pkg_data in installed_data:
				pkg = DNFPackage(pkg_data)
				if pkg.name in self._packages:
					# Update with installed info
					self._packages[pkg.name].data.update(pkg_data)
				else:
					self._packages[pkg.name] = pkg

		except (subprocess.CalledProcessError, json.JSONDecodeError):
			# Fallback to simple package list
			self._load_packages_fallback()

	def _load_packages_fallback(self) -> None:
		"""Fallback method to load packages without JSON."""
		try:
			result = subprocess.run(
				["dnf", "list", "--available"],
				capture_output=True,
				text=True,
				check=True
			)
			
			for line in result.stdout.split('\n'):
				if '.' in line and not line.startswith(('Available', 'Installed', 'Last')):
					parts = line.split()
					if len(parts) >= 3:
						name = parts[0].split('.')[0]
						version = parts[1]
						repo = parts[2] if len(parts) > 2 else "unknown"
						
						pkg_data = {
							"name": name,
							"version": version,
							"repo": repo,
							"arch": parts[0].split('.')[-1] if '.' in parts[0] else "x86_64"
						}
						self._packages[name] = DNFPackage(pkg_data)

		except subprocess.CalledProcessError:
			pass

	def __getitem__(self, name: str) -> DNFPackage:
		"""Get package by name."""
		if not self._loaded:
			self.open()
		
		if name in self._packages:
			return self._packages[name]
		
		# Try to get package info on demand
		try:
			result = subprocess.run(
				["dnf", "info", name],
				capture_output=True,
				text=True,
				check=True
			)
			
			# Parse dnf info output
			pkg_data = {"name": name}
			for line in result.stdout.split('\n'):
				if ':' in line:
					key, value = line.split(':', 1)
					key = key.strip().lower()
					value = value.strip()
					
					if key == "version":
						pkg_data["version"] = value
					elif key == "release":
						pkg_data["release"] = value
					elif key == "architecture":
						pkg_data["arch"] = value
					elif key == "summary":
						pkg_data["summary"] = value
					elif key == "description":
						pkg_data["description"] = value
					elif key == "size":
						pkg_data["size"] = value
					elif key == "from repo":
						pkg_data["repo"] = value

			pkg = DNFPackage(pkg_data)
			self._packages[name] = pkg
			return pkg
			
		except subprocess.CalledProcessError:
			raise KeyError(f"Package '{name}' not found")

	def __contains__(self, name: str) -> bool:
		"""Check if package exists in cache."""
		try:
			self[name]
			return True
		except KeyError:
			return False

	def __iter__(self):
		"""Iterate over packages."""
		if not self._loaded:
			self.open()
		return iter(self._packages.values())

	def keys(self):
		"""Get package names."""
		if not self._loaded:
			self.open()
		return self._packages.keys()

	def commit(self, progress=None) -> bool:
		"""Commit changes (install/remove packages)."""
		# This would be handled by the higher-level nala functions
		# that call dnf install/remove commands
		return True


def run_dnf_command(command: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
	"""Run a DNF command with proper error handling."""
	full_command = ["dnf"] + command
	
	# Force English output for DNF commands
	env = {
		**os.environ,
		"LANG": "en_US.UTF-8",
		"LC_ALL": "en_US.UTF-8"
	}
	
	try:
		result = subprocess.run(
			full_command,
			capture_output=capture_output,
			text=True,
			check=False,
			env=env
		)
		return result
	except Exception as e:
		raise RuntimeError(f"Failed to run DNF command: {e}")


# Create module-level instances to mimic apt_pkg structure
config = DNFConfig()
cache = DNFCache()