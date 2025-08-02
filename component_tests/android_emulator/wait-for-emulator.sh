#!/bin/bash
set -e

command -v adb || { echo "❌ adb not found"; exit 1; }

MAX_RETRIES=120
SLEEP_INTERVAL=2

echo "Waiting for emulator to be detected by adb..."

RETRY=0
while true; do
  echo "Checking adb devices... (try $((RETRY+1))/$MAX_RETRIES)"
  adb devices
  ADB_STATUS=$(adb devices | grep -w emulator | grep -w device || true)

  if [ -n "$ADB_STATUS" ]; then
    echo "Emulator is online: $ADB_STATUS"
    break
  fi

  if [ $RETRY -ge $MAX_RETRIES ]; then
    echo "Timed out waiting for emulator to show up via adb."
    exit 1
  fi

  RETRY=$((RETRY+1))
  sleep $SLEEP_INTERVAL
done

echo "Waiting for Appium server to report readiness..."

RETRY=0
while true; do
  echo "Checking Appium status at http://127.0.0.1:4723/status (try $((RETRY+1))/$MAX_RETRIES)"
  RESPONSE=$(curl -s http://127.0.0.1:4723/status || true)
  echo "Appium response: $RESPONSE"

  if echo "$RESPONSE" | grep -q '"ready"[[:space:]]*:[[:space:]]*true'; then
    echo "Appium is ready!"
    break
  fi

  if [ $RETRY -ge $MAX_RETRIES ]; then
    echo "Timed out waiting for Appium readiness."
    exit 1
  fi

  RETRY=$((RETRY+1))
  sleep $SLEEP_INTERVAL
done
