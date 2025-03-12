# Foxpass MAC Update Utility

## Description
This script interfaces with the Foxpass API to manage MAC address groups and entries. It enables automated management of MAC-based access control for your network environment.

---

## Prerequisites
- Python 3.12.9 (recommended)
- [Foxpass API Key](https://docs.foxpass.com/docs/api/)

---

## Installation and Setup

To get started, clone this repository and navigate to the project directory:

```bash
git clone https://github.com/mrzepa/foxpass_mac_update.git
cd foxpass_mac_update
```

Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

### Environment Variables
Create a `.env` file at the root of your project directory to store your Foxpass API Key securely.

`.env` file example:
```bash
FOXPASS_API_KEY=your_foxpass_api_key_here
```

Replace `your_foxpass_api_key_here` with your actual Foxpass API key.

### config.py Setup
Make a copy of the file `config.py.SAMPLE` and rename it to `config.py`:

```bash
cp config.py.SAMPLE config.py
```

Inside `config.py`, edit any of the following directories to meet your needs:

```python
import os

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
CACHE_DIR = 'cache'
BACKUP_DIR = 'backup'

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
```

> **Note:** Ensure the paths you specify are appropriate for your environment.

---

## Usage

The script requires two mandatory arguments:

- `--mac-group`: The name of the MAC group (Foxpass MAC entry group).
- `--mac-address-file`: A file containing the MAC addresses you wish to manage.

**Example usage**:

```bash
python foxpass_mac_update.py --mac-group your-mac-group --mac-address-file your-macs.txt
```

Replace:
- `your-mac-group` with your actual Foxpass MAC Entry group name.
- `your-macs.txt` with the filename containing your MAC addresses (placed in the `INPUT_DIR`, as defined in your `config.py`).

### Creating the MAC Address File

Create a plain text file with each MAC address listed on a separate line (no other characters or separators). For example, your file should look like this:

**your-macs.txt**
```text
00:1A:2B:3C:4D:5E
acb1.1234.aabb
99-11-aa-bb-9a-8c
8b2c3d4a556d
```

**Where to place the file**:
- Place your created MAC address file (`your-macs.txt`, or whatever your filename is) inside the designated input directory (`INPUT_DIR`) as specified in your `config.py`.  
  (Default path if unchanged is the `input/` directory at the project root.)

**Example command with default settings**:
Assuming the default `input/` directory:
```bash
python foxpass_mac_update.py --mac-group OfficeWiFi --mac-address-file mac_list.txt
```

---

## Project Structure
- `foxpass_mac_update.py`: Main script file that manages API interactions.
- `config.py`: Project configuration settings (Copied from `config.py.SAMPLE`).
- `.env`: Contains environment variables needed for API authorization.
- Input files (such as your MAC address file) stored in the `input/` folder.

---

## Troubleshooting
- **API Authentication Issues:**
  Verify that your Foxpass API key in `.env` is correct.
- **File Not Found issues:** Ensure your input files are placed in the correct `INPUT_DIR` as set in `config.py`.
- **MAC Address Validation Errors:** Ensure your MAC addresses match the expected format (e.g., `AA:BB:CC:DD:EE:FF`) without extra characters or spaces.

---

## Security Considerations
Always keep your `.env` file and API keys secure. Do not commit sensitive files to version control. Use `.gitignore` to protect these files:

```bash
echo '.env' >> .gitignore
```

---

## Contributing
Please follow the standard fork, branch, and PR model for contributing.

---
