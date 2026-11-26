@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0.."

echo ============================================
echo   打包泡泡哥商品管理工具 exe
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 goto NOPYTHON

python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 goto INSTALL
goto BUILD

:INSTALL
echo 正在安装 PyInstaller...
python -m pip install pyinstaller
if errorlevel 1 goto PIPFAIL
echo.

:BUILD
echo 正在打包，第一次可能需要 1-3 分钟...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "泡泡哥商品管理工具" --icon "%~dp0app.ico" --distpath "%~dp0dist" --workpath "%~dp0build" --specpath "%~dp0." "%~dp0product_admin.py"
if errorlevel 1 goto BUILDFAIL

echo.
echo 打包完成！exe 已生成到 tools\dist 目录。
echo.
echo 下一步可以打包分发包：
echo   python tools\make_package.py
echo.
pause
goto END

:NOPYTHON
echo [错误] 没有找到 python，请先安装 Python 3.10 或更高版本。
echo 安装时记得勾选 "Add python.exe to PATH"。
echo.
pause
goto END

:PIPFAIL
echo.
echo [错误] PyInstaller 安装失败，请检查网络后重试。
echo 也可以手动执行：python -m pip install pyinstaller
echo.
pause
goto END

:BUILDFAIL
echo.
echo [错误] 打包失败，请把上面的报错信息发给管理员。
echo.
pause
goto END

:END
endlocal
