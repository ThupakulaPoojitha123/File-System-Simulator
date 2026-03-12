# File System Simulator

## Description
In-memory file system simulator with directory and file operations.

## Features
- Create directories and files
- Read/write file content
- List directory contents
- Path-based navigation

## Usage
```python
fs = FileSystem()
fs.mkdir("/path/to/dir")
fs.touch("/path/to/file.txt")
fs.write("/path/to/file.txt", "content")
content = fs.read("/path/to/file.txt")
```

## Run
```bash
python filesystem.py
```
