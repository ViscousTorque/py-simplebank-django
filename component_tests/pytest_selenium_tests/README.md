# Selenium


```
wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
tar -xzf geckodriver-v0.36.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
geckodriver --version
sudo apt update
sudo apt install xvfb -y
```

## Trying with Chrome

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # Fix dependencies if needed
google-chrome --version  # Verify installation

wget https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
chromedriver --version  # Verify installation

sudo rm /usr/local/bin/chromedriver

CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}.0.6998.88/linux64/chromedriver-linux64.zip


unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

