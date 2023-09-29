OS="`uname`"
TARGET="src/py_dss_interface/dll/x64"
if [[ "$OS" == "Linux" ]]; then
	cp ../OpenDSS/Source/CMD/test/libopendssdirect.so $TARGET
        cp ../klusolve/Lib/libklusolve.so $TARGET
elif [[ "$OS" == "Darwin" ]]; then
	cp ../OpenDSS/Source/CMD/test/libopendssdirect.dylib $TARGET
        cp ../KLUSolve/Lib/libklusolve.dylib $TARGET
        install_name_tool -add_rpath @loader_path/. $TARGET/libopendssdirect.dylib
fi
