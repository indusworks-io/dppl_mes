# BACKUP

#!/usr/bin/env bash
set -euo pipefail

# === CONFIG ===
SITE="production.soundseal.in"                          # your Frappe site name
COMPOSE_FILE="/home/ubuntu/dppl/frappe_docker/pwd.yml"
BACKUP_DIR="/home/ubuntu/dppl/backups"
LOGFILE="${BACKUP_DIR}/backup.log"
RETENTION_DAYS=14
BACKUP_NAME="dppl_backup_$(date +'%Y-%m-%d_%H-%M')"
TAR_PATH="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"

DOCKER_BIN="/usr/bin/docker"
PATH="/usr/local/bin:/usr/bin:/bin"

echo "=== Backup started at $(date '+%F %T') ===" >> "$LOGFILE"

# Get container ID of backend service
CONTAINER_ID=$($DOCKER_BIN compose -f "$COMPOSE_FILE" ps -q backend || true)
if [[ -z "$CONTAINER_ID" ]]; then
    echo "ERROR: Backend container not running." | tee -a "$LOGFILE"
    exit 1
fi

echo "Backend container: $CONTAINER_ID" >> "$LOGFILE"

# Run Frappe backup inside container
$DOCKER_BIN exec "$CONTAINER_ID" bash -lc "cd /home/frappe/frappe-bench && bench --site ${SITE} backup --with-files" >> "$LOGFILE" 2>&1

# Determine paths
BACKUP_CONTAINER_DIR="/home/frappe/frappe-bench/sites/${SITE}/private/backups"

# Find the latest SQL dump created
LATEST_SQL=$($DOCKER_BIN exec "$CONTAINER_ID" bash -lc "ls -1t ${BACKUP_CONTAINER_DIR}/*.sql.gz | head -n1" | tr -d '\r\n')

if [[ -z "$LATEST_SQL" ]]; then
    echo "ERROR: No SQL backup file found inside container!" | tee -a "$LOGFILE"
    exit 1
fi

echo "Latest SQL backup: $LATEST_SQL" >> "$LOGFILE"

# Create a temporary directory for assembling the backup
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# Copy SQL backup + site files + configs to temp folder
$DOCKER_BIN cp "${CONTAINER_ID}:${LATEST_SQL}" "${TMP_DIR}/"
$DOCKER_BIN cp "${CONTAINER_ID}:/home/frappe/frappe-bench/sites/${SITE}" "${TMP_DIR}/${SITE}"

# Optionally include logs
$DOCKER_BIN cp "${CONTAINER_ID}:/home/frappe/frappe-bench/logs" "${TMP_DIR}/logs" || true

# Create a single tar.gz archive
tar -czf "$TAR_PATH" -C "$TMP_DIR" .
chmod 640 "$TAR_PATH"

echo "Created archive: $TAR_PATH" >> "$LOGFILE"

# Retention cleanup
find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +"$RETENTION_DAYS" -delete -print >> "$LOGFILE" 2>&1 || true

echo "Backup completed successfully at $(date '+%F %T')" >> "$LOGFILE"
echo "" >> "$LOGFILE"

# RESTORE
#!/usr/bin/env bash
set -euo pipefail

# === CONFIG ===
SITE="production.soundseal.in"
COMPOSE_FILE="/home/ubuntu/dppl/frappe_docker/pwd.yml"
BACKUP_DIR="/home/ubuntu/dppl/backups"
DOCKER_BIN="/usr/bin/docker"
PATH="/usr/local/bin:/usr/bin:/bin"

echo ""
echo "=== Frappe Site Restore Utility ==="
echo ""

# --- Step 1: Check backup file ---
echo "Available backup files:"
ls -1t ${BACKUP_DIR}/*.tar.gz 2>/dev/null || { echo "No backup files found in ${BACKUP_DIR}"; exit 1; }

read -rp "Enter the full backup filename (with .tar.gz): " BACKUP_FILE
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

if [[ ! -f "$BACKUP_PATH" ]]; then
  echo "Backup file not found: $BACKUP_PATH"
  exit 1
fi

echo "Using backup: $BACKUP_PATH"
echo ""

# --- Step 2: Ensure containers are up ---
cd /home/ubuntu/dppl/frappe_docker
$DOCKER_BIN compose -f "$COMPOSE_FILE" up -d
sleep 5

CONTAINER_ID=$($DOCKER_BIN compose -f "$COMPOSE_FILE" ps -q backend)
if [[ -z "$CONTAINER_ID" ]]; then
  echo "Backend container not found. Make sure your stack is running."
  exit 1
fi
echo "Backend container detected: $CONTAINER_ID"
echo ""

# --- Step 3: Extract backup locally ---
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT
echo "Extracting backup archive..."
tar -xzf "$BACKUP_PATH" -C "$TMP_DIR"
echo "Extracted into: $TMP_DIR"
echo ""

# --- Step 4: Detect backup components ---
SQL_FILE=$(find "$TMP_DIR" -type f -name "*.sql.gz" -print -quit)
if [[ -z "$SQL_FILE" ]]; then
  echo "ERROR: No .sql.gz file found in backup."
  exit 1
fi
echo "SQL dump file found: $SQL_FILE"

if [[ ! -d "$TMP_DIR/$SITE" ]]; then
  echo "ERROR: Site folder $SITE not found in backup."
  exit 1
fi

# --- Step 5: Copy data into container ---
echo "Copying files into backend container..."
$DOCKER_BIN exec "$CONTAINER_ID" bash -lc "rm -rf /home/frappe/frappe-bench/sites/${SITE}" || true
$DOCKER_BIN cp "$TMP_DIR/$SITE" "$CONTAINER_ID:/home/frappe/frappe-bench/sites/"
$DOCKER_BIN cp "$SQL_FILE" "$CONTAINER_ID:/home/frappe/frappe-bench/sites/${SITE}/private/backups/"
echo "Files copied."
echo ""

# --- Step 6: Restore inside container ---
echo "Restoring site inside container..."
$DOCKER_BIN exec -it "$CONTAINER_ID" bash -lc "
cd /home/frappe/frappe-bench &&
if [ ! -d sites/${SITE} ]; then
  echo 'Creating site ${SITE}...'
  bench new-site ${SITE} --mariadb-user-host-login-scope=% --db-root-password=admin --admin-password=admin --force
fi &&
SQL_PATH=\$(ls -1t sites/${SITE}/private/backups/*.sql.gz | head -n1) &&
echo 'Restoring database from:' \$SQL_PATH &&
bench --site ${SITE} --force restore \$SQL_PATH &&
echo 'Database restored.' &&
echo 'Restoring private and public files...' &&
cp -r sites/${SITE}/private/backups/private/files sites/${SITE}/private/ || true &&
cp -r sites/${SITE}/private/backups/public/files sites/${SITE}/public/ || true &&
echo 'Files restored successfully.'
"

echo ""
echo "=== Restore completed successfully! ==="
echo "You can now access your site at: http://<your-server-ip>:8080"
echo ""
