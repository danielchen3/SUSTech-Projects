from cx_Freeze import setup, Executable

# 配置包含的文件和目录
build_exe_options = {
    "packages": ["os", "sys", "PyQt5"],
    "includes": ["chooser", "function", "login_window"],
    "include_files": [("src/background.png", "src/background.png")],
}

# 配置生成的可执行文件
executables = [
    Executable(
        "main.py",
        base="Win32GUI",  # 指定为 GUI 应用程序，避免弹出控制台窗口
        target_name="main.exe"
    )
]

# 设置打包配置
setup(
    name="MainApp",
    version="0.1",
    description="My PyQt5 Application",
    options={"build_exe": build_exe_options},
    executables=executables
)
