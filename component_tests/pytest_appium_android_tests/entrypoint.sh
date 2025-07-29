#!/bin/bash
set -e

echo "Waiting for Appium to be ready..."
until curl -sf http://android-emulator:4723/status | grep -q '"ready":true'; do
  sleep 2
done

echo "Running tests..."
pytest component_tests/pytest_appium_android_tests/test_login.py -v --trace-config

