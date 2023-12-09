Unicode False
!addplugindir "./"
!include LogicLib.nsh

; The name of the installer
Name "autoLabel Installer"

; Set the output file name
OutFile "autoLabelInstaller.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\autoLabel"

; Create the installation directory
Section
  SetOutPath $INSTDIR
SectionEnd

; Function to delete specific files in the installation directory
Function DeleteInstallationContents
  SetOutPath $INSTDIR
  RMDir /r "$INSTDIR\*.*"
FunctionEnd

; Add the files and directories to the installer
Section
  Call DeleteInstallationContents ;Call the function to delete specific files
  SetOutPath $INSTDIR
  File /r "EHSA_V3\*.*"
  CreateDirectory "$INSTDIR\output"
SectionEnd

; Create a shortcut for ehsa_frontend.exe on the desktop
Section
  SetOutPath "$INSTDIR\bin"
  CreateShortCut "$DESKTOP\autoLabel.lnk" "$INSTDIR\hackathon.exe"
  ShellLink::SetRunAsAdministrator $DESKTOP\autoLabel.lnk
SectionEnd

; Call the CheckVCRedist function
Function .onInit
  Call CheckVCRedist
FunctionEnd

; Install VC++ Redist
Function InstallVCRedist
  ; Download the VC++ Redist installer
  NSISdl::download "https://aka.ms/vs/17/release/vc_redist.x64.exe" "$TEMP\vc_redist.x64.exe"
  ; Run the installer
  ExecWait "$TEMP\vc_redist.x64.exe /q"
  ; Check if the installation was successful
  ReadRegDWORD $0 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Installed"
  ; If the installation was not successful, prompt the user to try again
  ${If} $0 == ""
    MessageBox MB_RETRYCANCEL "VC++ Redist installation failed. Do you want to try again?" IDRETRY retry 
    retry:
        Call InstallVCRedist
  ${EndIf}
FunctionEnd

Function CheckVCRedist
  ; Check if the registry key exists
  ReadRegDWORD $0 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Installed"
  ; If the key does not exist, prompt the user to install VC++ Redist
  ${If} $0 == ""
    MessageBox MB_YESNO "This application requires VC++ Redist. Do you want to install it now?" IDYES install_vc_redist
    install_vc_redist:
        Call InstallVCRedist
  ${EndIf}
FunctionEnd
