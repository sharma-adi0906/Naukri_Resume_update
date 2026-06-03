$action  = New-ScheduledTaskAction `
    -Execute "C:\Python314\python.exe" `
    -Argument "C:\Users\sharm\Desktop\naukri resume automation\naukri_refresh.py" `
    -WorkingDirectory "C:\Users\sharm\Desktop\naukri resume automation"

$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5) `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName   "Naukri Daily Resume Upload" `
    -Action     $action `
    -Trigger    $trigger `
    -Settings   $settings `
    -RunLevel   Highest `
    -Force