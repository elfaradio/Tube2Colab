# Tube2Colab

Tube2Colab is a Python tool that extracts Google Colab notebook links from a YouTube playlist and automatically downloads the notebooks.

## Features

- Extracts all videos from a YouTube playlist
- Scans video descriptions for Google Colab links
- Supports:
  - Google Drive Colab notebooks
  - GitHub-based Colab notebooks
- Removes duplicate links
- Saves all links to a text file
- Automatically downloads `.ipynb` files
- Skips private or unavailable videos safely

## Requirements

- Python 3.8+
- yt-dlp
- requests

## Installation

```bash
pip install yt-dlp requests
```
