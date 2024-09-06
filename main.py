import json

import Riven_ocr

image_path = "static\\enhanced_2222.png"
res = Riven_ocr.RivenOcr(image_path)
print(res.ocr_list)

print(res.comparison_list)
