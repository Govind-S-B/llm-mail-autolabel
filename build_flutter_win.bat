cd flutter_frontend
call flutter build windows
cd ../
rmdir /s /q binary_build\data
move flutter_frontend\build\windows\x64\runner\Release\data binary_build
move flutter_frontend\build\windows\x64\runner\Release\hackathon.exe binary_build 
move flutter_frontend\build\windows\x64\runner\Release\flutter_windows.dll binary_build 