echo "Checking for installed programs"

$ErrorActionPreference = "Stop"

echo "Checking Kumir"
./embark.exe dqi "(Кумир|.{5}) 2.1.0-rc11" --ignore-version
if (0 -ne $LastExitCode) {
    echo "No Kumir found"
    exit 1
}

echo "Checking PascalABC.NET"
./embark.exe dqi "PascalABC.NET" --publisher "" --ignore-version
if (0 -ne $LastExitCode) {
    echo "No PascalABC.NET found"
    exit 1
}

echo "Checking LibreOffice"
./embark.exe dqi "LibreOffice [0-9\\.]*" --publisher "The Document Foundation" --version "403177474"
if (0 -ne $LastExitCode) {
    echo "No LibreOffice found"
    exit 1
}

echo "Checking CodeBlocks"
./embark.exe dqi "CodeBlocks" --publisher "The Code::Blocks Team" --version "20.03"
if (0 -ne $LastExitCode) {
    echo "No CodeBlocks found"
    exit 1
}

echo "Checking Chrome"
./embark.exe dqi "Google Chrome" --publisher "Google LLC" --ignore-version
if (0 -ne $LastExitCode) {
    echo "No Chrome found"
    exit 1
}

echo "Checking PyCharm"
./embark.exe dqi "PyCharm .*" --publisher "JetBrains s.r.o." --ignore-version
if (0 -ne $LastExitCode) {
    echo "No PyCharm found"
    exit 1
}

echo "Checking IntelliJ"
./embark.exe dqi "IntelliJ IDEA .*" --publisher "JetBrains s.r.o." --ignore-version
if (0 -ne $LastExitCode) {
    echo "No IntelliJ found"
    exit 1
}
