#!/bin/bash

WATCH_DIR="src"
TEST_CMD="./test.sh"
CHECKSUM_FILE="/tmp/dir_checksum"

# Function to generate a combined checksum of all Python files in the watch directory
get_checksum() {
    # find "$WATCH_DIR" -type f -name "*.py"  - Find all .py files in src directory
    # -exec md5sum {} \;                     - Run md5sum on each file found
    # 2>/dev/null                            - Discard error messages (e.g., if files are deleted during execution)
    # | md5sum                               - Create a single hash from all individual file hashes
    # Result: One hash representing the state of all Python files
    find "$WATCH_DIR" -type f -name "*.py" -exec md5sum {} \; 2>/dev/null | md5sum
}

echo "Watching $WATCH_DIR for changes (polling every 2 seconds)..."

# Get initial checksum and save it to a temporary file
get_checksum > "$CHECKSUM_FILE"

while true; do
    sleep 2
    
    # Get current state checksum
    NEW_CHECKSUM=$(get_checksum)
    # Read previous state checksum from file
    OLD_CHECKSUM=$(cat "$CHECKSUM_FILE")
    
    # Compare checksums - if different, files have changed
    if [ "$NEW_CHECKSUM" != "$OLD_CHECKSUM" ]; then
        echo "File changed, running tests..."
        $TEST_CMD
        echo "---"
        # Update stored checksum with new state
        echo "$NEW_CHECKSUM" > "$CHECKSUM_FILE"
    fi
done
