check:
	isort --check login.py
	black --check login.py
	typos login.py

fix:
	isort login.py
	black login.py
	typos -w login.py
