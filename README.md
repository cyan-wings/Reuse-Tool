# Reuse Assessmeent Tool

Author:       Matthew Yeow

Supervision:  Chong Chun Yong / Lim Mei Kuan

Description:
This is a project to supplement the author's PhD thesis work.
This project is currently hosted on [Render](https://reuse-assessment.streamlit.app/).

## Installation and Create Environment

1. Download latest release.
2. Extract the downloaded archive file.
```bash
cd streamlit-test
```

Alternatively:
```bash
git clone cyan-wings/streamlit-test
cd streamlit-test
```

#### Linux/macOS
Install JDK 11 (Any JDK will do. This tutorial we will use OpenJDK.) and Python (Latest version).
```bash
sudo apt-get install openjdk-11-jdk
sudo apt-get install python3
```

Create virtual environment for the application.
```bash
python3 -m venv venv-reuse-tool
source venv-reuse-tool/bin/activate
```

Install Python package dependencies for application.
```bash
python3 -m pip install -r requirements.txt
```

#### Windows
Install Java 11
Install Python

Install Python package dependencies for application.
```bash
python3 -m pip install -r requirements.txt
```

## Running the Application

```bash
python3 -m streamlit run About.py
```

Open Brave, Chrome or FireFox browser and input localhost:8501

## Stopping the Application

1. Ctrl-C to terminate the process on terminal.
2. Deactivate environment.

```bash
deactivate
```

## Uninstall Everything and Removing Application

1. Delete entire repository from folder.
2. Uninstall JDK 11 and Python.

## TODO

- Refactor code to have more structured modules along with code comments.
- Provide links in to the Maven Repositories in the Ranking page.
