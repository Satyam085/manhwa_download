import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from fpdf import FPDF

def download_images(url, headers,folder_path):
    # Send a GET request to the website
    response = requests.get(url,headers=headers)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the image tags on the page
    images = soup.find_all('img')

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Download and save filtered images
    for index, image in enumerate(images):
        image_url = image['src']
        print(image_url)
        image_name = f"image{index:02}.jpg"  # You can customize the image names as needed
        image_path = os.path.join(folder_path, image_name)

        # Send a GET request to download the image
        image_response = requests.get(image_url)

        # Save the image to the specified folder
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        # Check image height
        image_height = get_image_height(image_path)
        if image_height is not None and image_height > 5000:
            print(f"Downloaded {image_name} (height: {image_height}px)")
        else:
            os.remove(image_path)  # Delete the image if height requirement is not met
            print(f"Skipped {image_name} (height: {image_height}px)")

    # Convert images to a single PDF
    convert_to_pdf(folder_path)

    # Delete the image files
    delete_images(folder_path)

def get_image_height(image_path):
    try:
        with Image.open(image_path) as img:
            return img.height
    except (IOError, OSError):
        return None

def convert_to_pdf(folder_path):
    pdf_path = os.path.join(folder_path, f'{file_name}.pdf')

    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Sort the image files based on their names
    image_files.sort()

    # Create a PDF object
    pdf = FPDF()

    # Disable auto page breaks
    pdf.set_auto_page_break(auto=True, margin=0)

    # Convert each image to a PDF page and add it to the PDF object
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image_width, image_height = get_image_dimensions(image_path)

        if image_width is not None and image_height is not None:
            # Set the page dimensions
           # pdf.set_page_dimensions(image_width, image_height)
            pdf.add_page(orientation='portrait',format=[image_width,image_height])

            # Add the image to the PDF
            pdf.image(image_path, x=0, y=0, w=image_width, h=image_height)

    # Save the PDF file
    pdf.output(pdf_path)

    print(f"PDF file created at {pdf_path}")


def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            return img.size
    except (IOError, OSError):
        return None, None

def delete_images(folder_path):
    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Delete each image file
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        os.remove(image_path)

    print("All image files deleted.")


# Send a GET request to the website
url = 'https://www.asurascans.com/the-tutorial-is-too-hard-chapter-115/'
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'}

file_name = url.split('/')[-2]

# Provide the path to the folder where you want to save the images
folder_path = 'images'  # Update with the desired folder path

# Call the function to download and save the images
download_images(url, headers, folder_path)
