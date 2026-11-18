# Secure File Transfer Monitoring System

## Project Overview
This project monitors files in a selected folder to detect file activities and identify potential security concerns.

## Features
- File creation, modification, deletion, and movement monitoring.
- SHA-256 file integrity checking.
- Detection of changes in file contents.
- Sensitive filename alerts.
- Security audit logging.
- Automatic integrity report generation.
- Security activity summary.

## Technologies Used
- Python
- Visual Studio Code
- Watchdog
- SHA-256 hashing
- JSON
- Logging

## Project Structure
- monitor.py - Monitors file activities.
- integrity.py - Calculates SHA-256 hashes.
- integrity_report.py - Generates file integrity reports.
- change_detector.py - Detects file changes.
- security_audit.py - Records security audit events.
- security_summary.py - Generates security activity summaries.
- monitored_files/ - Folder containing files to monitor.
- logs/ - Folder containing logs and reports.

## How to Run

1. Open the project folder in VS Code.
2. Start file monitoring:
   python monitor.py
3. Generate an integrity report:
   python integrity_report.py
4. Check for file changes:
   python change_detector.py
5. Generate the security summary:
   python security_summary.py

## Purpose
The goal of this project is to improve file integrity monitoring, detect suspicious file-related activity, and maintain security audit records.