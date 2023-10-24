import fitz
import os

def extract_and_save_images_from_pdf_with_pymupdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    
    # Убедитесь, что папка для сохранения существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_links = []
    
    for current_page in range(pdf_document.page_count):
        page = pdf_document.load_page(current_page)
        images = page.get_images(full=True)
        
        for image_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            image_path = os.path.join(output_folder, f"page{current_page + 1}_img{image_index + 1}.png")
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            
            image_links.append(image_path)
            
    return image_links

pdf_path = 'admi.pdf'
image_links = extract_and_save_images_from_pdf_with_pymupdf(pdf_path, 'output_images')

# Вывод локальных "ссылок" на изображения
for link in image_links:
    print(link)
