# Gut Tracker

## Directory

gut_health_tracker/
├── app/
│   ├── main.py          # Entry point for the Kivy app
│   ├── __init__.py      # Makes the app directory a Python package
│   ├── models.py        # Data models (e.g., bowel movement records)
│   ├── views.py         # UI components and screens
│   ├── utils.py         # Utility functions (e.g., data processing)
│   └── assets/          # Static files
│       ├── images/      # Icons, backgrounds, etc.
│       └── sounds/      # Audio files (if any)
├── tests/
│   ├── test_models.py   # Tests for data models
│   ├── test_views.py    # Tests for UI components
│   └── ...
├── buildozer.spec       # Configuration file for building the APK
├── README.md            # Project documentation
├── LICENSE              # License file
└── requirements.txt     # Python dependencies (e.g., kivy, sqlite3)

## Setup Hints

For SQLCipher:
sudo apt-get install libsqlcipher-dev 

For Java 17 (compaitble with Gradle):
sudo apt-get install openjdk-17-jdk
sudo update-alternatives --config java

For .NET Core SDK:
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu focal main universe"
sudo apt-get update
sudo apt-get install libicu66
sudo apt-get install -y dotnet-sdk-7.0
