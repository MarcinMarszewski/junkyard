Set-ExecutionPolicy Bypass -Scope Process -Force

[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))					# install chocolatey

[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ProgramData\chocolatey\bin", "Machine")				# add choco to path
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")							# update path



choco install firefox														# install vscode
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Mozilla Firefox", "Machine")			# add firefox to path
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")							# update path
firefox.exe -silent -nosplash -setDefaultBrowser										# set firefox as default browser

choco install vscode														# install vscode
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Microsoft VS Code\bin", "Machine")			# add vscode to path
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")							# update path

choco install steam														# install steam
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files (x86)\Steam", "Machine")				# add steam to path
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")							# update path

choco install discord
# Discord installation seems hard to automate



choco install python313
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Python313;C:\Python313\Scripts", "Machine")			
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

choco install openjdk
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\OpenJDK\jdk-22.0.2\bin", "Machine")		
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

choco install git
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Git\cmd", "Machine")		
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

choco install 7zip
C:\Program Files\7-Zip

choco install wireguard
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\WireGuard", "Machine")		
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

choco install bitwarden


Todo    
    email



Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "HideFileExt" -Value 0		# Visible file extensions
Stop-Process -Name explorer -Force
Start-Process explorer														# Reset explorer



$Bloatware = @(

        #Unnecessary Windows 10 AppX Apps
        "Microsoft.BingNews"
        "Microsoft.GetHelp"
        "Microsoft.Getstarted"
        "Microsoft.Messaging"
        "Microsoft.Microsoft3DViewer"
        "Microsoft.MicrosoftOfficeHub"
        "Microsoft.MicrosoftSolitaireCollection"
        "Microsoft.NetworkSpeedTest"
        "Microsoft.News"
        "Microsoft.Office.Lens"
        "Microsoft.Office.OneNote"
        "Microsoft.Office.Sway"
        "Microsoft.OneConnect"
        "Microsoft.People"
        "Microsoft.Print3D"
        "Microsoft.RemoteDesktop"
        "Microsoft.SkypeApp"
        "Microsoft.StorePurchaseApp"
        "Microsoft.Office.Todo.List"
        "Microsoft.Whiteboard"
        "Microsoft.WindowsAlarms"
        #"Microsoft.WindowsCamera"
        "microsoft.windowscommunicationsapps"
        "Microsoft.WindowsFeedbackHub"
        "Microsoft.WindowsMaps"
        "Microsoft.WindowsSoundRecorder"
        "Microsoft.Xbox.TCUI"
        "Microsoft.XboxApp"
        "Microsoft.XboxGameOverlay"
        "Microsoft.XboxIdentityProvider"
        "Microsoft.XboxSpeechToTextOverlay"
        "Microsoft.ZuneMusic"
        "Microsoft.ZuneVideo"

        #Sponsored Windows 10 AppX Apps
        #Add sponsored/featured apps to remove in the "*AppName*" format
        "*EclipseManager*"
        "*ActiproSoftwareLLC*"
        "*AdobeSystemsIncorporated.AdobePhotoshopExpress*"
        "*Duolingo-LearnLanguagesforFree*"
        "*PandoraMediaInc*"
        "*CandyCrush*"
        "*BubbleWitch3Saga*"
        "*Wunderlist*"
        "*Flipboard*"
        "*Twitter*"
        "*Facebook*"
        "*Spotify*"
        "*Minecraft*"
        "*Royal Revolt*"
        "*Sway*"
        "*Speed Test*"
        "*Dolby*"
             
        #Optional: Typically not removed but you can if you need to for some reason
        #"*Microsoft.Advertising.Xaml_10.1712.5.0_x64__8wekyb3d8bbwe*"
        #"*Microsoft.Advertising.Xaml_10.1712.5.0_x86__8wekyb3d8bbwe*"
        #"*Microsoft.BingWeather*"
        #"*Microsoft.MSPaint*"
        #"*Microsoft.MicrosoftStickyNotes*"
        #"*Microsoft.Windows.Photos*"
        #"*Microsoft.WindowsCalculator*"
        #"*Microsoft.WindowsStore*"
    )
    foreach ($Bloat in $Bloatware) {
        Get-AppxPackage -Name $Bloat| Remove-AppxPackage
        Get-AppxProvisionedPackage -Online | Where-Object DisplayName -like $Bloat | Remove-AppxProvisionedPackage -Online
        Write-Output "Trying to remove $Bloat."
    }


    Write-Output "Disabling Windows Feedback Experience program"
    $Advertising = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo"
    If (Test-Path $Advertising) {
        Set-ItemProperty $Advertising Enabled -Value 0 
    }

    Write-Output "Stopping Cortana from being used as part of your Windows Search Function"
    $Search = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    If (Test-Path $Search) {
        Set-ItemProperty $Search AllowCortana -Value 0 
    }

    Write-Output "Disabling Bing Search in Start Menu"
    $WebSearch = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    Set-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" BingSearchEnabled -Value 0 
    If (!(Test-Path $WebSearch)) {
        New-Item $WebSearch
    }
    Set-ItemProperty $WebSearch DisableWebSearch -Value 1 

    Write-Output "Turning off Data Collection"
    $DataCollection1 = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection"
    $DataCollection2 = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
    $DataCollection3 = "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\DataCollection"    
    If (Test-Path $DataCollection1) {
        Set-ItemProperty $DataCollection1  AllowTelemetry -Value 0 
    }
    If (Test-Path $DataCollection2) {
        Set-ItemProperty $DataCollection2  AllowTelemetry -Value 0 
    }
    If (Test-Path $DataCollection3) {
        Set-ItemProperty $DataCollection3  AllowTelemetry -Value 0 
    }

# Download other debloaters
# I advise to read the code before running scripts

git clone https://github.com/Sycnex/Windows10Debloater.git