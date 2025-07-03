const { app, BrowserWindow, shell, Menu, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const net = require('net');

let mainWindow;
let streamlitProcess;

function createWindow() {
  // Determine icon path based on environment
  let iconPath;
  if (app.isPackaged) {
    // Production: use bundled resources
    iconPath = path.join(process.resourcesPath, 'images/icon.png');
  } else {
    // Development: use local files
    iconPath = path.join(__dirname, '../images/icon.png');
  }

  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      enableRemoteModule: false,
      spellcheck: false
    },
    title: 'Lacework Compliance Reporter',
    show: false, // Don't show until ready
    icon: iconPath
  });

  // Show loading page first
  mainWindow.loadFile('index.html');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Check port availability before starting Streamlit
  checkPortAndStart();
}

function checkPortAvailability(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    
    server.listen(port, () => {
      server.once('close', () => {
        resolve(true); // Port is available
      });
      server.close();
    });
    
    server.on('error', () => {
      resolve(false); // Port is in use
    });
  });
}

function checkPortAndStart() {
  checkPortAvailability(8501).then(isAvailable => {
    if (isAvailable) {
      startStreamlit();
    } else {
      // Port is in use, show warning dialog
      dialog.showMessageBox(mainWindow, {
        type: 'warning',
        title: 'Port Already in Use',
        message: 'Port 8501 is already in use',
        detail: 'Another application is using port 8501. Please close any other instances of Lacework Compliance Reporter or other applications using this port, then restart the application.',
        buttons: ['OK', 'Retry', 'Quit'],
        defaultId: 0
      }).then((result) => {
        if (result.response === 1) {
          // Retry
          setTimeout(checkPortAndStart, 1000);
        } else if (result.response === 2) {
          // Quit
          app.quit();
        }
      });
    }
  });
}

function startStreamlit() {
  const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
  let streamlitPath;
  let workingDir;
  
  // Check if we're running in development or production
  if (app.isPackaged) {
    // Production: use bundled resources
    workingDir = path.join(process.resourcesPath, '.');
    if (process.platform === 'win32') {
      streamlitPath = path.join(workingDir, 'venv/Scripts/streamlit.exe');
    } else {
      streamlitPath = path.join(workingDir, 'venv/bin/streamlit');
    }
  } else {
    // Development: use local files
    workingDir = path.join(__dirname, '..');
    if (process.platform === 'win32') {
      streamlitPath = path.join(workingDir, 'venv/Scripts/streamlit.exe');
    } else {
      streamlitPath = path.join(workingDir, 'venv/bin/streamlit');
    }
  }

  // Log to file instead of console in production
  if (!app.isPackaged) {
    console.log('Starting Streamlit with path:', streamlitPath);
    console.log('Working directory:', workingDir);
  }

  streamlitProcess = spawn(streamlitPath, [
    'run',
    path.join(workingDir, 'streamlit_app.py'),
    '--server.port=8501',
    '--server.headless=true',
    '--browser.gatherUsageStats=false',
    '--server.enableCORS=false',
    '--server.enableXsrfProtection=false'
  ], {
    cwd: workingDir
  });

  streamlitProcess.stdout.on('data', (data) => {
    if (!app.isPackaged) {
      console.log(`Streamlit: ${data}`);
    }
    if (data.toString().includes('Local URL: http://localhost:8501')) {
      // Streamlit is ready, load the app
      setTimeout(() => {
        mainWindow.loadURL('http://localhost:8501');
      }, 2000);
    }
  });

  streamlitProcess.stderr.on('data', (data) => {
    if (!app.isPackaged) {
      console.error(`Streamlit Error: ${data}`);
    }
  });

  streamlitProcess.on('error', (error) => {
    if (!app.isPackaged) {
      console.error('Failed to start Streamlit:', error);
    }
    mainWindow.loadFile('error.html');
  });
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Reload',
          accelerator: 'CmdOrCtrl+R',
          click: () => mainWindow.reload()
        },
        {
          label: 'Developer Tools',
          accelerator: 'F12',
          click: () => mainWindow.webContents.toggleDevTools()
        },
        { type: 'separator' },
        {
          label: 'Quit',
          accelerator: 'CmdOrCtrl+Q',
          click: () => app.quit()
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'selectall' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About Lacework Compliance Reporter',
          click: () => {
            const packageJson = require('./package.json');
            require('electron').dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About',
              message: 'Lacework Compliance Reporter',
              detail: `Version ${packageJson.version}\nA modern compliance reporting tool for Lacework`
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

app.whenReady().then(() => {
  createMenu();
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  if (streamlitProcess) {
    if (!app.isPackaged) {
      console.log('Stopping Streamlit process...');
    }
    streamlitProcess.kill();
  }
});

// Handle app quit
app.on('quit', () => {
  if (streamlitProcess) {
    streamlitProcess.kill();
  }
}); 