enter:
	echo "The Nala-Fedora MakeFile"

install:
	# Install Python dependencies for Fedora
	sudo dnf install -y python3-pip python3-devel rpm-devel
	pip3 install --user .

	# Install man pages (if available)
	# sudo ./nala_build.py man --install

	# Install translations (if available)
	# sudo python3 -m pip install babel
	# sudo ./nala_build.py babel --compile --install

	make completions
	make config

completions:
	# Create Shell Completion Directories for Fedora

	sudo mkdir -p /usr/share/fish/vendor_completions.d/
	sudo mkdir -p /usr/share/bash-completion/completions/
	sudo mkdir -p /usr/share/zsh/site-functions/

	# Install shell completions (if available)
	# Note: These would need to be adapted for nala-fedora
	# sudo cp debian/nala.fish /usr/share/fish/vendor_completions.d/nala-fedora.fish
	# sudo cp debian/bash-completion /usr/share/bash-completion/completions/nala-fedora
	# sudo cp debian/_nala /usr/share/zsh/site-functions/_nala-fedora

config:
	# Install the Nala-Fedora Configuration file.
	sudo mkdir -p /etc/nala
	sudo cp nala.conf /etc/nala/nala.conf

clean:
	rm -f docs/nala*.8
	rm -rf ./.venv

uninstall:
	# sudo rm -f /usr/share/man/man8/nala*8.gz
	sudo rm -rf /etc/nala
	pip3 uninstall -y nala-fedora

binary:
	# Build binary (if needed)
	# ./nala-pyinstall.sh
