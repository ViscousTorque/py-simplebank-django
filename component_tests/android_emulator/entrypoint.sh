#!/bin/bash
set -e

# Resolve frontend hostname to host gateway
HOST_GATEWAY=$(ip route | awk '/default/ { print $3 }')
echo "$HOST_GATEWAY frontend" >> /etc/hosts

echo "Accepting SDK licenses..."
yes | sdkmanager --licenses

echo "Creating AVD..."
sdkmanager --install "system-images;android-33;google_apis;x86_64" --verbose
echo "no" | avdmanager create avd -n ci_emulator -k "system-images;android-33;google_apis;x86_64" --device "pixel"

# Optionally override RAM and disable snapshots
echo "hw.ramSize=1024" >> /root/.android/avd/ci_emulator.avd/config.ini
echo "snapshot.present=false" >> /root/.android/avd/ci_emulator.avd/config.ini

echo "Starting Android emulator..."
$ANDROID_SDK_ROOT/emulator/emulator -avd ci_emulator -memory 1024 -no-audio -no-window -gpu swiftshader_indirect -no-snapshot &

echo "Waiting for emulator to boot..."
$ANDROID_SDK_ROOT/platform-tools/adb wait-for-device
$ANDROID_SDK_ROOT/platform-tools/adb shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'

echo "Emulator booted."

echo "Starting Appium..."
appium server