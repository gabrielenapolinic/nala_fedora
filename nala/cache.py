#                 __
#    ____ _____  |  | _____
#   /    \\__  \ |  | \__  \
#  |   |  \/ __ \|  |__/ __ \_
#  |___|  (____  /____(____  /
#       \/     \/          \/
#
# Copyright (C) 2021, 2022 Blake Lee
#
# This file is part of nala
#
# nala is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nala is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with nala.  If not, see <https://www.gnu.org/licenses/>.
"""The Cache subclass module."""
from __future__ import annotations

import contextlib
import fnmatch
import sys
from typing import TYPE_CHECKING, Generator

# import apt_pkg  # Replaced with dnf_interface
# from apt.cache import Cache as _Cache  # Replaced with dnf_interface
# from apt.package import Package  # Replaced with dnf_interface

from nala import _, color, color_version
from nala.dnf_interface import DNFCache as _Cache, DNFPackage as Package
from nala.constants import ERROR_PREFIX, NOTICE_PREFIX, WARNING_PREFIX
from nala.options import arguments
from nala.rich import Columns, from_ansi
from nala.utils import dprint, eprint, term

if TYPE_CHECKING:
	from nala.debfile import NalaDebPackage
	from nala.dpkg import InstallProgress, UpdateProgress


PACKAGES_CAN_BE_UPGRADED = "\n" + _("The following {total} packages can be upgraded:")
NOT_CANDIDATE = color("[") + color(_("Not candidate version"), "YELLOW") + color("]")


class Cache(_Cache):
	"""Subclass of apt.cache to add features."""

	def commit_pkgs(
		self,
		install_progress: InstallProgress,
		update_progress: UpdateProgress,
		local_debs: list[NalaDebPackage] | None = None,
	) -> bool:
		"""Apply the marked changes to the cache."""
		# For DNF, this would be handled by calling dnf install/remove commands
		# The actual implementation would depend on the marked packages
		return self.commit(progress=install_progress)

	def is_secret_virtual(self, pkg_name: str) -> bool:
		"""Return True if the package is secret virtual.

		For DNF, this concept is less relevant as virtual packages work differently.
		"""
		try:
			pkg = self[pkg_name]
			# In DNF context, a package either exists or doesn't
			return False
		except KeyError:
			return True

	def is_any_virtual(self, pkgname: str) -> bool:
		"""Return whether the package is a virtual package.

		For DNF, virtual packages are handled differently.
		"""
		try:
			pkg = self[pkgname]
		except KeyError:
			return False
		# In DNF, packages exist or they don't - virtual packages are less common
		return False

	def glob_filter(self, pkg_names: list[str], show: bool = False) -> list[str]:
		"""Filter provided packages and glob *.

		Returns a new list of packages matching the glob.

		If there is nothing to glob it returns the original list.
		"""
		if "*" not in f"{pkg_names}":
			return pkg_names

		new_packages: list[str] = []
		glob_failed = False
		for pkg_name in pkg_names:
			if "*" in pkg_name:
				dprint(f"Globbing: {pkg_name}")
				glob = fnmatch.filter(self.get_pkg_names(show), pkg_name)
				if not glob:
					glob_failed = True
					eprint(
						_(
							"{error} unable to find any packages by globbing {pkg}"
						).format(error=ERROR_PREFIX, pkg=color(pkg_name, "YELLOW"))
					)
					continue
				new_packages.extend(glob)
			else:
				new_packages.append(pkg_name)

		if glob_failed:
			sys.exit(1)
		new_packages.sort()
		dprint(f"List after globbing: {new_packages}")
		return new_packages

	def get_pkg_names(self, show: bool = False) -> Generator[str, None, None]:
		"""Generate all real packages, or packages that can provide something."""
		# For DNF, we just iterate over available package names
		for pkg_name in self.keys():
			yield pkg_name

	def virtual_filter(self, pkg_names: list[str], remove: bool = False) -> list[str]:
		"""Filter package to check if they're virtual."""
		new_names = set()
		for pkg_name in pkg_names:
			if pkg_name in self:
				new_names.add(pkg_name)
				continue
			if (vpkg := self.check_virtual(pkg_name, remove)) and isinstance(
				vpkg, Package
			):
				new_names.add(vpkg.name)
				continue
			new_names.add(pkg_name)
		dprint(f"Virtual Filter: {new_names}")
		return sorted(new_names)

	def what_replaces(self, pkg_name: str) -> Generator[str, None, None]:
		"""Generate packages that replace the given name."""
		# For DNF, replacement information is not as easily accessible
		# This would require querying DNF for obsoletes information
		return
		yield  # Make this a generator

	def check_virtual(self, pkg_name: str, remove: bool = False) -> Package | bool:
		"""Check if the package is virtual."""
		# For DNF, virtual packages are less common
		# Most packages either exist or don't exist
		if pkg_name in self:
			return self[pkg_name]
		return False

	def purge_removed(self) -> None:
		"""Make sure everything marked as removed is getting purged."""
		if not arguments.is_purge():
			return
		# For DNF, purging is handled differently
		# DNF doesn't have the same concept as APT's purge
		pass

	def protect_upgrade_pkgs(self, exclude: list[str] | None) -> set[Package]:
		"""Mark excluded packages as protected."""
		protected: set[Package] = set()
		if not exclude:
			return protected
		# For DNF, package protection would be handled differently
		# This would likely involve DNF exclude commands
		for pkg_name in self.glob_filter(exclude):
			if pkg_name in self:
				pkg = self[pkg_name]
				print(
					_("Protecting {package} from changes").format(
						package=color(pkg_name, "GREEN")
					)
				)
				protected.add(pkg)
		return protected

	def upgradable_pkgs(self) -> Generator[Package, None, None]:
		"""Generate upgradable packages."""
		# For DNF, we need to check if packages have newer versions available
		for pkg in self:
			if pkg.installed and pkg.version != pkg.installed_version:
				yield pkg

	def print_upgradable(self) -> None:
		"""Print packages that are upgradable."""
		if arguments.config.get_bool("update_show_packages"):
			if upgradable := [
				# format will look like "python3-pip (22.1.1-1) -> (22.2-1)"
				from_ansi(
					f"{color(pkg.name, 'GREEN')} "
					f"{color_version(pkg.installed_version or 'unknown')} -> {color_version(pkg.version)}"
				)
				for pkg in self.upgradable_pkgs()
				if pkg.installed
			]:
				print(PACKAGES_CAN_BE_UPGRADED.format(total=color(len(upgradable))))
				term.console.print(Columns(upgradable, padding=(0, 2), equal=True))
				return

		elif total_pkgs := len(tuple(self.upgradable_pkgs())):
			print(
				_(
					"{total} packages can be upgraded. Run '{command}' to see them."
				).format(
					total=color(total_pkgs, "YELLOW"),
					command=color("nala list --upgradable", "GREEN"),
				)
			)
			return

		print(color(_("All packages are up to date.")))


def install_archives(
	apt: any | list[str], install_progress: InstallProgress
) -> int:
	"""Install the archives using DNF."""
	install_progress.start_update()

	# For DNF, this would call dnf commands directly
	try:
		res = install_progress.run_install(apt)
	finally:
		pass

	install_progress.finish_update()
	return res


def print_virtual_pkg(
	pkg_name: str, provides: list[Package], not_candidate: bool = False
) -> None:
	"""Print the virtual package string."""
	print(
		_("{package} is a virtual package provided by:").format(
			package=color(pkg_name, "GREEN")
		)
	)
	print(
		"".join(
			[
				f"\n  {color(pkg.name, 'GREEN')} {color_version(pkg.candidate.version)} "
				f"{NOT_CANDIDATE if not_candidate else ''}"
				for pkg in provides
				if pkg.candidate
			]
		).strip("\n")
	)
	print(_("You should select just one."))


def print_selecting_pkg(provider: str, pkg_name: str) -> None:
	"""Print that we are selecting a different package."""
	print(
		_(
			"{notice} Selecting {provider}\n  Instead of virtual package {package}"
		).format(
			notice=NOTICE_PREFIX,
			provider=color(provider, "GREEN"),
			package=color(pkg_name, "GREEN"),
		),
		end="\n\n",
	)
