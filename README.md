# AndRoversing
Tools for easier Android app reversing

<b>find_code_calls.py</b><br/>
helps to find static strings obfuscations and deobfuscate them dynamically using frida for Android note: it assumes that frida for Android configured properly amd there is connected device/emulator

<b>print_packages.py<b/><br/>
helps to find common packages (SDKs) between group of apps. simply provide directory with all the APKs you want to check.

<b>replace_smali_classes.py<b><br/>
looks for Java source file metadata in smali bytecode in order to try deobfuscate some of the classes in app to more meaningful names. you should provide a smali code directory.
