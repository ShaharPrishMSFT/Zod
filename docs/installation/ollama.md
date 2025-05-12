# Ollama Installation Guide

This guide covers the installation and configuration of Ollama, a local Large Language Model runtime.

## System Requirements

- Windows 10/11 64-bit
- Minimum 8GB RAM (16GB recommended)
- Storage space for models (varies by model size)

## Installation Steps

1. Download Ollama:
   - Visit [Ollama's official website](https://ollama.ai/download)
   - Download the Windows installer

2. Run the installer:
   - Default installation path: `C:\Users\shaharp\appdata\local\Programs\Ollama\ollama.exe`
   - Follow the installation wizard's instructions

3. Service Configuration:
   - Ollama runs as a Windows service on port 11434
   - Service starts automatically with Windows
   - Manual start if needed: `.\ollama.exe serve`

## Model Installation

Currently configured to use:
```bash
# Install the default model
ollama pull tinyllama:latest

# Model specifications:
# - Family: llama
# - Parameters: 1B
# - Quantization: Q4_0
```

## Verification

Test the installation by running:
```powershell
# Test service endpoint
curl http://localhost:11434/api/tags

# Test model
.\ollama.exe run tinyllama "Hello, world!"
```

## API Usage

The Ollama API is available at `http://localhost:11434`. Example usage:

```powershell
# PowerShell example
$body = @{
    model='tinyllama'
    prompt='Your prompt here'
} | ConvertTo-Json

curl -X POST http://localhost:11434/api/generate `
    -H 'Content-Type: application/json' `
    -d $body
```

## Troubleshooting

1. Service not starting:
   - Check Windows Services
   - Try manual start: `.\ollama.exe serve`

2. Port conflicts:
   - Verify no other service is using port 11434
   - Check firewall settings

3. Model issues:
   - Verify model installation: `ollama list`
   - Try reinstalling: `ollama pull tinyllama:latest`
