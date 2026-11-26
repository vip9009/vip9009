@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0.."

echo ============================================
echo   泡泡哥雾化 - 商品管理工具
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 goto NOPYTHON

python -c "import PIL" >nul 2>nul
if errorlevel 1 goto INSTALL
goto RUN

:INSTALL
echo [提示] 首次运行，正在安装图片处理依赖 Pillow...
python -m pip install -r tools\requirements.txt
if errorlevel 1 goto PIPFAIL
echo.

:RUN
echo 正在启动工具...
python tools\product_admin.py
if errorlevel 1 goto RUNFAIL
goto END

:NOPYTHON
echo [错误] 没有找到 python，请先安装 Python 3.10 或更高版本。
echo 安装时记得勾选 "Add Python to PATH"。
echo.
pause
goto END

:PIPFAIL
echo.
echo [错误] 依赖安装失败，请检查网络后重试。
echo 也可以手动执行：python -m pip install -r tools\requirements.txt
echo.
pause
goto END

:RUNFAIL
echo.
echo [错误] 工具异常退出，请把上面的报错信息发给管理员。
echo.
pause

:END
endlocal
