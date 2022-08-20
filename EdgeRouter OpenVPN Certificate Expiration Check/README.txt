EdgeRouter OpenVPN Certificate Expiration Check

This check checks all .pem files in /config/auth/ and it's subfolders of a Ubiquiti EdgeRouter for their expiration date.
It runs on Debian based servers with Python 3.

How to install:
  1. Create a SSH key for the monitoring user on the EdgeRouter.
  2. Create a monitoring user and configure the key on the router:
     # set system login user monitoring authentication public-keys monitoring type ssh-rsa
     # set system login user monitoring authentication public-keys monitoring key [public key string]
  3. Place the check file in /usr/lib/check_mk_agent/local and make it executable.
  4. Install the paramiko Python library (sudo -H pip install paramiko).
  5. Place the private key file next to the check script and 'chmod 600' it.
  6. Configure your EdgeRouter's IP, monitoring user, keyfile name and the warning/critical limits in the check script file.
