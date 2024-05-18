setlocal

cd D:\Raspberry Pi Service Backups\.utils

:: Get current date in yyyy-mm-dd format
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x

if %Day% lss 10 set Day=0%Day%
if %Month% lss 10 set Month=0%Month%

set today=%Year%-%Month%-%Day%

echo %today%

:: Generate the filename
set filename=services-%today%.zip

:: Remote Linux machine details
set remote_user=aleksandar
set remote_host=192.168.100.3
set remote_path=~/services
:: Windows machine details
set local_path=D:/"Raspberry Pi Service Backups"

if exist %local_path%/%filename% (
	exit /b 0
)

:: SCP command
set scp_command=scp %remote_user%@%remote_host%:%remote_path%/%filename% %local_path%

:: Execute SCP command
%scp_command%

endlocal