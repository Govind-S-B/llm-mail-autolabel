python -m PyInstaller --onefile python_label_core/auto_label.py
del pdf_generator.spec
robocopy dist binary_build /IS
rmdir /s /q "build"
rmdir /s /q "dist"