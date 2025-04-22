echo "Checking for installed programs"

$ErrorActionPreference = "Stop"

echo "Checking Kumir"
./embark.exe dqi "Кумир 2.1.0-rc11" --ignore-version

echo "Checking PascalABC.NET"
./embark.exe dqi "PascalABC.NET" --publisher "" --ignore-version

echo "Checking LibreOffice"
./embark.exe dqi"LibreOffice [0-9\\.]*" --publisher "The Document Foundation" --version "403177474"

echo "Checking CodeBlocks"
./embark.exe dqi "CodeBlocks" --publisher "The Code::Blocks Team" --version "20.03"

echo "Checking Chrome"
./embark.exe dqi "Google Chrome" --publisher "Google LLC" --ignore-version

echo "Checking JDK"
./embark.exe dqi "Java .* 23 (64-bit)" --publisher "Oracle Corporation" --version "23.0.0.0"

echo "Checking PyCharm"
./embark.exe dqi "PyCharm .*" --publisher "JetBrains s.r.o." --ignore-version

echo "Checking IntelliJ"
./embark.exe dqi "IntelliJ IDEA .*" --publisher "JetBrains s.r.o." --ignore-version

echo $LastExitCode
exit $LastExitCode
