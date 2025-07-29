#!/bin/bash
set -e

# resolve frontend hostname to host gateway
HOST_GATEWAY=$(ip route | awk '/default/ { print $3 }')
echo "$HOST_GATEWAY frontend" >> /etc/hosts

echo "Starting Android emulator..."
$ANDROID_SDK_ROOT/emulator/emulator -avd ci_emulator -no-audio -no-window -gpu swiftshader_indirect -no-snapshot &

echo "Waiting for emulator to boot..."
$ANDROID_SDK_ROOT/platform-tools/adb wait-for-device
$ANDROID_SDK_ROOT/platform-tools/adb shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'

echo "Emulator booted."

echo "Starting Appium..."
appium server