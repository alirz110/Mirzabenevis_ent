import os

# --- تنظیمات ---
# پوشه‌ها و فایل‌هایی که می‌خواهید نادیده گرفته شوند
IGNORE_DIRECTORIES = {'.git', '__pycache__', 'venv', '.vscode', 'node_modules', 'dist', 'build'}
IGNORE_FILES = {'.DS_Store', '.env'}
# ---------------

def generate_tree(root_dir):
    """
    ساختار درختی یک پوشه را به همراه فایل‌هایش تولید و چاپ می‌کند.
    """
    if not os.path.isdir(root_dir):
        print(f"خطا: مسیر '{root_dir}' یک پوشه معتبر نیست.")
        return

    # استخراج نام پوشه اصلی برای شروع
    root_name = os.path.basename(os.path.abspath(root_dir))
    print(f"{root_name}/")

    _recursive_tree_builder(root_dir, "")

def _recursive_tree_builder(directory, prefix=""):
    """
    تابع بازگشتی برای پیمایش و چاپ ساختار پوشه.
    """
    try:
        # دریافت لیست فایل‌ها و پوشه‌ها و فیلتر کردن موارد نادیدنی
        entries = [e for e in os.listdir(directory) if e not in IGNORE_FILES]
        dirs = sorted([d for d in entries if os.path.isdir(os.path.join(directory, d)) and d not in IGNORE_DIRECTORIES])
        files = sorted([f for f in entries if os.path.isfile(os.path.join(directory, f))])
    except PermissionError:
        print(f"{prefix}└── [عدم دسترسی به پوشه]")
        return

    all_items = dirs + files
    total_items = len(all_items)

    for i, item in enumerate(all_items):
        is_last = (i == total_items - 1)
        connector = "└── " if is_last else "├── "
        
        print(f"{prefix}{connector}{item}")

        # اگر آیتم یک پوشه بود، به صورت بازگشتی داخل آن می‌رویم
        if item in dirs:
            new_prefix = prefix + ("    " if is_last else "│   ")
            _recursive_tree_builder(os.path.join(directory, item), new_prefix)

if __name__ == "__main__":
    # دریافت مسیر پروژه از کاربر
    project_path = input("لطفاً مسیر کامل پوشه پروژه خود را وارد کنید و Enter را بزنید: ")
    
    print("\n======================================")
    print("ساختار پروژه شما:")
    print("======================================\n")
    
    generate_tree(project_path)
    
    print("\n======================================")
    print("کپی کردن این ساختار و ارسال آن کافی است.")