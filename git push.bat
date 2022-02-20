for /f "tokens=1-4 delims=/ " %%i in ("%date%") do (
     set date=%%i

)
call git add -A

call git commit -m %date%

call git push

pause