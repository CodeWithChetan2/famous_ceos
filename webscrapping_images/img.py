from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time




wd = webdriver.Chrome()



def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)
	url="https://www.google.com/search?q=warren+buffet&tbm=isch&ved=2ahUKEwi77sX9xZaAAxUWrGMGHQA9DQ4Q2-cCegQIABAA&oq=warren+buffet&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyCAgAEIAEELEDMgUIABCABDIFCAAQgAQ6BAgjECc6BwgAEIoFEEM6BwgjEOoCECc6CggAEIoFELEDEEM6CwgAEIAEELEDEIMBOgcIABCABBAKOgYIABAFEB46BAgAEB46CAgAEAUQHhAKOgkIABAYEIAEEApQmwVYpVVgl1poBnAAeAGAAbwBiAHGGpIBBDAuMjmYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=75-1ZPu6M5bYjuMPgPq0cA&bih=714&biw=1536&rlz=1C1CHBD_enIN1057IN1057"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) +skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME,"r48jcc")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls
def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path +"\\"+ file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 50)

for i, url in enumerate(urls):
	download_image("C:\\Users\\chetr\\OneDrive\\Desktop\\famous_ceos\\webscrapping_images\\warren_buffet", url, "warren_buffet"+str(i) + ".jpg")

wd.quit()



