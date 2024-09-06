import Riven_ocr

image_path = "static\\lanka.jpg"
res = Riven_ocr.RivenOcr(image_path)
print(res.ocr_list)

print(res.comparison_list)
