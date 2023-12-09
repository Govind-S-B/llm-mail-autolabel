python -m PyInstaller --onefile python_label_core/auto_label.py
del auto_label.spec
robocopy dist binary_build /IS
rmdir /s /q "build"
rmdir /s /q "dist"