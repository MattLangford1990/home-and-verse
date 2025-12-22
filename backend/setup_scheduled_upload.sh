#!/bin/bash
# Setup script for scheduled Zoho upload
# Run with: sudo bash setup_scheduled_upload.sh

echo "Setting up scheduled Zoho upload for 3:00 AM..."

# Create the launchd plist
cat > /Users/matt/Library/LaunchAgents/com.homeandverse.zoho-upload.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.homeandverse.zoho-upload</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/matt/Desktop/home-and-verse/backend/scheduled_upload.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>5</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/zoho_launchd_out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/zoho_launchd_err.log</string>
</dict>
</plist>
EOF

# Fix ownership
chown matt:staff /Users/matt/Library/LaunchAgents/com.homeandverse.zoho-upload.plist

# Schedule Mac to wake at 3:00 AM
pmset schedule wake "12/15/2025 03:00:00"

# Load the launch agent
sudo -u matt launchctl load /Users/matt/Library/LaunchAgents/com.homeandverse.zoho-upload.plist

echo ""
echo "✅ Done! Your Mac will:"
echo "   1. Wake at 3:00 AM"
echo "   2. Run the upload script at 3:05 AM"
echo ""
echo "Check results tomorrow with:"
echo "   cat /tmp/zoho_scheduled_upload.log"
echo ""
echo "To remove the schedule later:"
echo "   launchctl unload ~/Library/LaunchAgents/com.homeandverse.zoho-upload.plist"
echo "   sudo pmset schedule cancelall"
