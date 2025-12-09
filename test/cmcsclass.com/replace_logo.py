import os
import shutil

# 定义目录和文件
base_dir = r"d:\ypm\my web\test\pangminybm.com\wp-content\uploads\2025\07"
source_logo = "cmcs(2).png"
target_files = [
    "FullColor_1280x1024_300dpi-1-150x150.webp",
    "FullColor_1280x1024_300dpi-1-300x240-removebg-preview.webp",
    "FullColor_1280x1024_300dpi-1-scaled.webp"
]

def replace_logos():
    src_path = os.path.join(base_dir, source_logo)
    
    # 检查源 Logo 是否存在
    if not os.path.exists(src_path):
        print(f"Error: Source logo '{source_logo}' not found in {base_dir}")
        return

    print(f"Source Logo: {src_path}")
    print("-" * 50)

    for target in target_files:
        target_path = os.path.join(base_dir, target)
        backup_path = target_path + ".bak"

        # 1. 备份 (如果尚未备份)
        if os.path.exists(target_path):
            if not os.path.exists(backup_path):
                try:
                    os.rename(target_path, backup_path)
                    print(f"[Backup]  {target} -> {target}.bak")
                except OSError as e:
                    print(f"[Error] Failed to backup {target}: {e}")
                    continue
            else:
                print(f"[Skip]    Backup already exists for {target}")
                # 如果备份已存在，我们假设当前的目标文件可能是之前的错误尝试，或者我们即便覆盖也没关系
                # 为了安全，我们还是要把当前的目标文件移走或者删除，以便放入新文件
                try:
                    os.remove(target_path)
                    print(f"[Remove]  Removed existing {target} to allow overwrite")
                except OSError:
                    pass
        else:
            print(f"[Info]    Target {target} does not exist (will create new)")

        # 2. 复制新 Logo
        try:
            shutil.copy2(src_path, target_path)
            print(f"[Replace] Copied cmcs.png -> {target}")
        except OSError as e:
            print(f"[Error]   Failed to copy logo to {target}: {e}")

    print("-" * 50)
    print("Logo replacement complete!")

if __name__ == "__main__":
    replace_logos()
