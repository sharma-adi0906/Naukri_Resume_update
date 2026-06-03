# Naukri_Resume_update
Auto-update your resume on naukri.com on one-click

Prerequisites:
    python installed with "Add python.exe to PATH" checked during installation.
    playwright installed:
        $ pip install playwright python-dotenv
        $ playwright install chromium


Clone this directory
edit .env file and mention the parameters(email, pwd, resume path)
    1. keep the Resume file in this working directory and then paste the path in .env
run the naukri_refresh.py everyday at 9 AM using below command on cmd:
    $ python naukri_refresh.py

You can schedule it also using "Task scheduler":

1. In the task-scheduler.ps1 file, be sure to paste the right path of python.exe, path can be checked using below command in windows cmd:
    $ where.exe python

2. To schedule this task on windows:
    copy whole content of task-scheduler.ps1 and run it on powershell (run as administrator)
    check if the task is scheduled using below command:
        Get-ScheduledTask -TaskName "Naukri Daily Resume Upload"
    Start the scheduled task using below:
        Start-ScheduledTask -TaskName "Naukri Daily Resume Upload"
    

