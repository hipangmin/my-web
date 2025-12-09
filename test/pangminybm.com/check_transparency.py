from PIL import Image

def check_transparency(image_path):
    try:
        img = Image.open(image_path)
        print(f"Image Mode: {img.mode}")
        
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # 检查是否有非 255 的 alpha 值
            if img.mode != 'P':
                extrema = img.getextrema()
                alpha_extrema = extrema[-1] # Alpha 通道的最大最小值
                print(f"Alpha Extrema: {alpha_extrema}")
                if alpha_extrema[0] < 255:
                    print("✅ Image has transparent pixels.")
                    return True
                else:
                    print("⚠️ Image has an alpha channel but appears fully opaque (no transparency).")
                    return False
            else:
                 print("✅ Image is in Palette mode with transparency info.")
                 return True
        else:
            print("❌ Image does not have an alpha channel (no transparency).")
            return False
            
    except Exception as e:
        print(f"Error checking image: {e}")
        return False

if __name__ == "__main__":
    check_transparency(r"d:\ypm\my web\test\pangminybm.com\wp-content\uploads\2025\07\cmcs(2).png")
