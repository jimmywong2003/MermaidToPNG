@echo off
echo ========================================
echo   MermaidToPNG - Quick Start
echo ========================================
echo.
echo This will convert the example document
echo and show you how to use the tool.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Converting example_document.md...
echo.

mermaid_to_png_converter.exe example_document.md

echo.
echo ========================================
echo   Conversion Complete!
echo ========================================
echo.
echo The diagrams have been saved to:
echo   example_document_diagrams/
echo.
echo To use with your own files, run:
echo   mermaid_to_png_converter.exe your_file.md
echo.
echo Press any key to exit...
pause >nul
