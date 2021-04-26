@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=docs

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

if "%1" == "html" (
	rem Prepare for Github Pages, that expects HTML files in the root
	rem Copy files from the html subdirectory to the build dir
	xcopy %BUILDDIR%\html %BUILDDIR%\ /s /d /y /q
	rem Disable automatic execution of Jekyill by GHPages
	xcopy .nojekyll %BUILDDIR%\ /d /y /q
)

goto end

if "%1" == "pdf" (
    %SPHINXBUILD% -b pdf -e dotted_toc %SOURCEDIR% %BUILDDIR%/pdf %SPHINXOPTS% %O%
    echo.
    echo.Build finished. The PDF files are in %BUILDDIR%/pdf
    goto end
)


:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
