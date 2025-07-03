# Lacework Compliance Reporter - Electron App

This directory contains the Electron wrapper for the Lacework Compliance Reporter Streamlit application.

## Setup

### Prerequisites
- Node.js (v16 or higher)
- npm (comes with Node.js)
- Python virtual environment with all dependencies installed

### Installation

1. **Install Node.js dependencies:**
   ```bash
   cd electron
   npm install
   ```

2. **Ensure Python environment is ready:**
   ```bash
   # From the root directory
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   
   pip install -r requirements.txt
   ```

## Development

### Start the Electron app in development mode:
```bash
cd electron
npm start
```

This will:
1. Start the Electron app
2. Show a loading screen
3. Start the Streamlit server
4. Load the Streamlit app in the Electron window

## Building for Distribution

### Build the application:
```bash
cd electron
npm run dist
```

This will create distributable packages in the `../dist` folder:
- **Windows**: `.exe` installer
- **macOS**: `.dmg` file  
- **Linux**: `.AppImage` file

### Build options:
- `npm run build` - Build without distribution
- `npm run dist` - Build with distribution packages

## Features

- **Native Desktop Experience**: Looks and feels like a desktop application
- **Loading Screen**: Professional loading animation while Streamlit starts
- **Error Handling**: Graceful error handling if Streamlit fails to start
- **Menu Bar**: Standard desktop application menu
- **External Links**: Opens external links in default browser
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Troubleshooting

### Streamlit won't start:
1. Ensure virtual environment is activated
2. Check that all dependencies are installed
3. Verify Streamlit is available: `streamlit --version`

### Build fails:
1. Ensure Node.js and npm are installed
2. Check that all dependencies are installed: `npm install`
3. Verify Python environment is properly set up

### App crashes on startup:
1. Check the console output for error messages
2. Ensure the virtual environment path is correct
3. Verify file permissions

## File Structure

```
electron/
├── main.js          # Main Electron process
├── preload.js       # Preload script for security
├── index.html       # Loading screen
├── error.html       # Error page
├── package.json     # Node.js configuration
└── README.md        # This file
```

## Configuration

The app automatically includes:
- `streamlit_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `config.example.json` - Configuration template
- `images/` - Application images
- `venv/` - Python virtual environment

## Security

- Context isolation enabled
- Node integration disabled
- External links opened in default browser
- Minimal preload script for security 