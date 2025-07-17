               Internet (DSL)
                     |
             [WiFi ADSL Modem/Router]
                |    |      \
      WiFi ------   |        \      
  (All devices)     |         WiFi (fallback)
                    |         
                    | (LAN port)
                    |
              [TP-Link LS1005G Switch]
         ________|_____|_____|_______
        |        |     |     |       |
 [Win Laptop 1]  |     |     |   [Xbox X]
 [Win Laptop 2]  |     |     |
 [Raspberry Pi]  |     |     |
 [Old MacBook (Ubuntu 22.04)]
     - Connection: Ethernet (via TP-Link Switch)
     - IP Address: 192.168.1.25
     - Speed: 1 Gbps
     - Status: Internet confirmed working
     - Role: Hosting web server, PostgreSQL, and a graph DB for internal use
     - PostgreSQL:
         - Running locally on port 5432
         - Default user: `postgres`
         - Accessed via: `sudo -u postgres psql`
         - Local-only access initially configured
         - Password set via `\password postgres` inside psql
         - Current password: `numipipdeedee`
         - Role-based access configured: role `almir` created with CREATEDB privilege
         - Remote access enabled: `listen_addresses = '*'` in postgresql.conf
         - LAN access permitted for 192.168.1.0/24 via `pg_hba.conf`
         - UFW was blocking port 5432 initially; rule added and reloaded
         - PostgreSQL service restarted after changes
         - Confirmed remote connection successful from Windows and WSL
         - Used for internal data storage and dev testing
     - Nginx:
         - Installed and running
         - Accessible at: `http://192.168.1.25`
     - Neo4j:
         - Installed and enabled
         - Configured for remote access
         - Accessible from LAN at: `http://192.168.1.25:7474`
         - Bolt port `7687` exposed and reachable
         - Default user: `neo4j` (password reset using `neo4j-admin` tool)
         - Confirmed login from external device successful
     - RabbitMQ:
         - Installed and running
         - Port 5672 (AMQP) accessible from LAN
         - Web UI on port 15672 (if enabled)
         - Custom user created with permission to access default vhost
         - Tested connection from WSL via Python `pika` client
         - Message queue `test` successfully used
     - SSH:
         - User: `almir`
         - Access via: `ssh almir@192.168.1.25`
     - Security:
         - UFW firewall installed and enabled
         - Allowed ports: 22 (SSH), 80 (HTTP), 7474 (Neo4j), 7687 (Neo4j Bolt), 5432 (PostgreSQL), 5672 (RabbitMQ AMQP)
         - All other ports blocked by default
         - `fail2ban` installed and running with default SSH protection
         - SSH access secured on default port 22 (LAN only)
     - Lid Behavior:
         - Configured to stay awake when lid is closed
         - `HandleLidSwitch=ignore` set in `/etc/systemd/logind.conf`
         - Confirmed system remains reachable over network with lid closed
         - Applied via `sudo systemctl restart systemd-logind`
     - Future Improvements:
         - Set up regular PostgreSQL backups
         - Optionally install `pgAdmin` for visual DB management
         - Document active passwords and user accounts securely
         - Set up monitoring with Netdata or Grafana
         - Add Pi-hole on Raspberry Pi for network-wide ad blocking
         - Segment devices using VLANs if switch supports it
         - Enable SSH rate limiting or move SSH to custom port
         - Automate updates/backups using cron scripts
         - Install Tailscale or Zerotier for secure remote access
         - Add UPS for power outage resilience
         - Evaluate message flows between Raspberry Pi, web server, and background processing