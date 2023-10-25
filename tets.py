import fitz
import os
import io

from PIL import Image, ImageDraw, ImageFont

def extract_and_save_images_from_pdf_with_pymupdf(pdf_path, output_file):
    pdf_document = fitz.open(pdf_path)
    
    images_to_merge = []
    
    for current_page in range(pdf_document.page_count):
        page = pdf_document.load_page(current_page)
        images = page.get_images(full=True)
        
        for image_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            image = Image.open(io.BytesIO(image_bytes))
            
            # Добавление пометки о номере страницы
            draw = ImageDraw.Draw(image)
            text = f"Page {current_page + 1}"
            font = ImageFont.truetype("arial.ttf", 15) # Указать путь к шрифту, если он отличается
            draw.text((10,10), text, font=font, fill=(255,0,0,255))
            
            images_to_merge.append(image)

    # Объединение всех изображений в одно
    total_height = sum(i.height for i in images_to_merge)
    max_width = max(i.width for i in images_to_merge)
    combined_image = Image.new('RGB', (max_width, total_height))
    
    y_offset = 0
    for im in images_to_merge:
        combined_image.paste(im, (0, y_offset))
        y_offset += im.height

    combined_image.save(output_file)
    return output_file

pdf_path = 'admi.pdf'
output_file = 'combined_images.png'
image_link = extract_and_save_images_from_pdf_with_pymupdf(pdf_path, output_file)

# Вывод локальной "ссылки" на объединенное изображение
print(image_link)
