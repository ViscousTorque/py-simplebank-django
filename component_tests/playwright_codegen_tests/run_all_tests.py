import subprocess
import sys
import pathlib

def main():
    test_dir = pathlib.Path("/app/component_tests/playwright_codegen_tests/tests")
    test_files = sorted(test_dir.glob("*.py"))
    print(test_files)

    if not test_files:
        print("❌ No test files found in 'tests/'")
        sys.exit(1)

    failures = 0

    for test_file in test_files:
        print(f"\n🚀 Running {test_file}")
        result = subprocess.run([sys.executable, str(test_file)])
        if result.returncode != 0:
            print(f"❌ Test {test_file.name} failed.")
            failures += 1
        else:
            print(f"✅ Test {test_file.name} passed.")

    if failures:
        print(f"\n❌ {failures} test(s) failed.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
