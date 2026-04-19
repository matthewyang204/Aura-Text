import os

def get_linux_productname():
    print("Getting Linux product name in order to apply quirks...", end='')
    with open("/sys/class/dmi/id/product_name") as f:
        product_name = f.read().strip()
    print(product_name)
    return product_name

def crosvm_quirks():
    print("Applying Chrome OS crostini quirks...")
    os.environ["QT_QPA_PLATFORM"] = "xcb"