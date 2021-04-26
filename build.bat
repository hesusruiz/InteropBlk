@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

set SOURCEDIR=.
set BUILDDIR=docs

if "%1" == "pdf" goto pdf

REM Build HTML (default)
sphinx-build %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:pdf
REM Build PDF with rinoh
sphinx-build -b rinoh %SOURCEDIR% %BUILDDIR%

:end
popd
