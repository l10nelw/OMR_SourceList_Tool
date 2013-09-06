@echo off

for %%f in (Rpt%%5FOnlineMediaReach.xls, "Source List template.xlsx") do (
	if not exist %%f (
		echo %%f does not exist
		pause
		goto :eof
	)
)
python makesourcelist0.py