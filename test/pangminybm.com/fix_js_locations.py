import os
import requests
import time

# 缺失的文件列表
files = [
    "carousel.3620fca501cb18163600.bundle.min.js",
    "nested-carousel.db797a097fdc5532ef4a.bundle.min.js",
    "nav-menu.8521a0597c50611efdc6.bundle.min.js",
    "text-editor.45609661e409413f1cef.bundle.min.js",
    "form.71055747203b48a65a24.bundle.min.js",
    "popup.f7b15b2ca565b152bf98.bundle.min.js",
    "media-carousel.8d26e5df1a1527329fde.bundle.min.js",
    "gallery.06be1c07b9901f53d709.bundle.min.js",
    "load-more.8b46f464e573feab5dd7.bundle.min.js",
    "posts.aec59265318492b89cb5.bundle.min.js",
    "portfolio.4cd5da34009c30cb5d70.bundle.min.js",
    "share-buttons.63d984f8c96d1e053bc0.bundle.min.js",
    "slides.c0029640cbdb48199471.bundle.min.js",
    "social.d71d263bd937f0906192.bundle.min.js",
    "table-of-contents.3be1ab725f562d10dd86.bundle.min.js",
    "archive-posts.16a93245d08246e5e540.bundle.min.js",
    "search-form.b7065999d77832a1b764.bundle.min.js",
    "woocommerce-menu-cart.54f2e75f6769dce707e2.bundle.min.js",
    "woocommerce-purchase-summary.88a2d8ca449739e34f9f.bundle.min.js",
    "woocommerce-checkout-page.6ba1f1f2aa99210fa1cf.bundle.min.js",
    "woocommerce-cart.480d117b95956d1f28a5.bundle.min.js",
    "woocommerce-my-account.d54826f355f9822b0ec0.bundle.min.js",
    "woocommerce-notices.00f9132bbbd683277a27.bundle.min.js",
    "product-add-to-cart.c32f5d5e404511d68720.bundle.min.js",
    "loop.89cc81d2188312a17a17.bundle.min.js",
    "loop-carousel.cd9a95b2e4dd2a239b81.bundle.min.js",
    "ajax-pagination.2090b5f4906bcda1dcc2.bundle.min.js",
    "mega-menu.82093824ddb3f5531ab4.bundle.min.js",
    "mega-menu-stretch-content.480e081cebe071d683e8.bundle.min.js",
    "menu-title-keyboard-handler.f0362773c21105d2c65c.bundle.min.js",
    "taxonomy-filter.a32526f3e4a201b5fce1.bundle.min.js",
    "off-canvas.137463f629e2b7cbaf02.bundle.min.js",
    "contact-buttons.99a987d66bcc2ade0ee6.bundle.min.js",
    "contact-buttons-var-10.16cf733dc3d3b250fef4.bundle.min.js",
    "floating-bars-var-2.75c36e8b0bacbac6105e.bundle.min.js",
    "floating-bars-var-3.cdf99fd0b063a0032d53.bundle.min.js",
    "search.5d88e65c03029f91931d.bundle.min.js",
    "stripe-button.49130d6eecb5ebc8afbd.bundle.min.js",
    "video-playlist.909c41acbc73cb741e9d.bundle.min.js",
    "paypal-button.f4f64e46173f50701949.bundle.min.js",
    "code-highlight.b9addbc842a50347c9ab.bundle.min.js",
    "progress-tracker.8cccdda9737c272489fc.bundle.min.js",
    "animated-headline.c009d6fa482515df23f8.bundle.min.js",
    "countdown.0e9e688751d29d07a8d3.bundle.min.js",
    "hotspot.5033ed75928eff79cb95.bundle.min.js",
    "lottie.a287ccfe024bea61e651.bundle.min.js",
    "shared-frontend-handlers.03caa53373b56d3bab67.bundle.min.js",
    "section-frontend-handlers.d85ab872da118940910d.bundle.min.js"
]

# 两个主要目录
dirs = {
    "pro": "wp-content/plugins/elementor-pro/assets/js/",
    "core": "wp-content/plugins/elementor/assets/js/"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for d in dirs.values():
    if not os.path.exists(d):
        os.makedirs(d)

import random

def download_with_retry(url, local_path):
    for i in range(3):
        try:
            print(f"Checking {url} (Attempt {i+1})...")
            time.sleep(random.uniform(1, 3))
            
            r = requests.head(url, headers=headers, timeout=10)
            if r.status_code == 404:
                return False
            
            if r.status_code == 200:
                print(f"⬇️ Downloading...")
                r = requests.get(url, headers=headers, timeout=20)
                with open(local_path, 'wb') as f:
                    f.write(r.content)
                print("✅ Success")
                return True
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)
    return False

for file in files:
    for type, dir_path in dirs.items():
        url = f"https://macmasterimaritime.com/{dir_path}{file}"
        local_path = os.path.join(dir_path, file)
        
        if os.path.exists(local_path):
            continue
            
        download_with_retry(url, local_path)
