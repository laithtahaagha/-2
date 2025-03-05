; نظام الأرشفة للدراسات العليا - ملف إعداد Inno Setup

#define MyAppName "نظام الأرشفة للدراسات العليا"
#define MyAppVersion "1.0"
#define MyAppPublisher "Laith Agha"
#define MyAppURL "https://www.example.com"
#define MyAppExeName "نظام الأرشفة للدراسات العليا.exe"

[Setup]
AppId={{C2A1D7DE-03D9-4343-83B0-8E7E0D53E47B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=Output
OutputBaseFilename=نظام_الأرشفة_للدراسات_العليا_Setup
SetupIconFile=generated-icon.png
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DirExists=alwaysoverwrite
PrivilegesRequired=admin


[Languages]
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\نظام الأرشفة للدراسات العليا\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent