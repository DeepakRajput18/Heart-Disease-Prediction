# Heart Disease Prediction System - Commands Guide

This document explains all available commands and how to run them.

## Quick Start

The simplest way to start the server:

```bash
# Using npm
npm start

# Or directly with Python
python3 minimal_server.py

# Or the ultra simple version
python3 ultra_simple.py
```

## Available Commands

### NPM Scripts

All these commands work with `npm run <command>`:

| Command | Description | Example |
|---------|-------------|---------|
| `start` | Start minimal server (recommended) | `npm start` |
| `dev` | Start development server with auto-reload | `npm run dev` |
| `simple` | Start ultra simple server | `npm run simple` |
| `setup` | Full setup (install + database) | `npm run setup` |
| `test` | Run all tests | `npm run test` |
| `init-db` | Initialize database | `npm run init-db` |
| `fix` | Run command fixer | `npm run fix` |
| `docker-build` | Build Docker image | `npm run docker-build` |
| `docker-run` | Run Docker container | `npm run docker-run` |
| `docker-compose-up` | Start with Docker Compose | `npm run docker-compose-up` |
| `docker-compose-down` | Stop Docker Compose | `npm run docker-compose-down` |

### Make Commands

If you prefer using Make:

```bash
make help           # Show all available commands
make start          # Start server (auto-detect)
make dev            # Start development server
make simple         # Start ultra simple server
make minimal        # Start minimal server
make full           # Start full server
make test           # Run tests
make init-db        # Initialize database
make install        # Install dependencies
make setup          # Full setup
make clean          # Clean temporary files
make docker-build   # Build Docker image
make docker-run     # Run Docker container
```

### Direct Python Scripts

You can also run Python scripts directly:

```bash
# Server options (in order of complexity)
python3 ultra_simple.py      # Simplest server
python3 minimal_server.py    # Minimal server with basic features
python3 run_server.py        # Development server
python3 start_server.py      # Universal server with auto-detection

# Utility scripts
python3 init_db.py           # Initialize database
python3 fix_commands.py      # Fix common command issues
python3 run_commands.py      # Universal command runner
python3 run.py               # New universal runner

# Example with run_commands.py
python3 run_commands.py start
python3 run_commands.py test
python3 run_commands.py init-db
```

### Universal Runner (run.py)

The new `run.py` script provides a unified interface:

```bash
python3 run.py install          # Install all dependencies
python3 run.py install-minimal  # Install minimal dependencies
python3 run.py setup            # Full setup
python3 run.py start            # Start minimal server
python3 run.py dev              # Start dev server
python3 run.py simple           # Start simple server
python3 run.py test             # Run tests
python3 run.py init-db          # Initialize database
python3 run.py fix              # Fix issues
python3 run.py docker-build     # Build Docker image
```

## Command Compatibility

### All Commands Work
✅ `npm start` - Start minimal server
✅ `npm run dev` - Start development server
✅ `npm run simple` - Start ultra simple server
✅ `npm run setup` - Setup system
✅ `npm run test` - Run tests (if pytest installed)
✅ `npm run init-db` - Initialize database (if MongoDB available)
✅ `npm run fix` - Run command fixer
✅ All docker commands (if Docker installed)

### Platform-Specific Scripts

**Unix/Linux/Mac:**
```bash
./start.sh          # Shell script to start server
./install.sh        # Shell script to install dependencies
```

**Windows:**
```cmd
start.bat           # Batch file to start server
install.bat         # Batch file to install dependencies
```

These platform-specific scripts are created by `fix_commands.py`.

## Troubleshooting

### If commands don't work:

1. **Run the fixer:**
   ```bash
   npm run fix
   # or
   python3 fix_commands.py
   ```

2. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.8+
   ```

3. **Try direct Python scripts:**
   ```bash
   python3 ultra_simple.py  # Simplest option
   ```

4. **Use Docker:**
   ```bash
   docker-compose up -d
   ```

### Common Issues

**"python3: command not found"**
- Install Python 3.8 or higher
- On Windows, use `py` instead of `python3`

**"No module named 'fastapi'"**
- Dependencies not installed
- Run: `npm run setup` or use Docker

**"pip not found"**
- pip is not available in your Python installation
- Use platform-specific installers or Docker

**Port 8000 already in use**
- Use the `start_server.py` script which auto-detects available ports:
  ```bash
  python3 start_server.py
  ```

## Recommended Workflow

### For Development:
```bash
# First time setup
npm run setup

# Start development server
npm run dev
```

### For Quick Testing:
```bash
# Just start the server
npm start
# or
npm run simple
```

### For Production:
```bash
# Use Docker
npm run docker-compose-up

# Or build and run directly
npm run docker-build
npm run docker-run
```

## Server Access

Once any server is running, access the application at:
- **URL:** http://localhost:8000
- **Login:** admin@heartpredict.com
- **Password:** admin123

## Additional Help

Run any command without arguments to see help:

```bash
python3 run_commands.py       # Shows help
python3 run.py                # Shows help
python3 start_server.py --help # Shows options
make help                     # Shows all make commands
```
