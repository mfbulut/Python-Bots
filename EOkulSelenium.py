tcNo = "1111111111"
schoolNo = "222"
birthday = "22"
birthmonth = "HAZIRAN"
birthyear = "2000"
birthDistrict = "MERAM"
birthCounty = "KONYA"
className = "B Şubesi"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image, ImageEnhance
from io import BytesIO
from SSIM_PIL import compare_ssim
import pytesseract

import time

import cv2
import numpy as np
from matplotlib import pyplot as plt

driver = webdriver.Edge()
driver.get("https://eokulyd.meb.gov.tr/")
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.find_element(By.CLASS_NAME, "btn-vg").click()
    time.sleep(6)
    driver.find_element(By.ID, "VBSKullanici").send_keys(tcNo)
    driver.find_element(By.ID, "VBSpassword").send_keys(schoolNo)
    driver.find_element(By.ID, "btnVBSGiris").click()

    firstQuestion = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/form/div[3]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/label/span",
            )
        )
    )

    secondtQuestion = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/label/span",
    )

    if firstQuestion.text == "Öğrencinin doğum yılı nedir?":
        driver.find_element(By.ID, "txtS1T1").send_keys(birthyear)

    if firstQuestion.text == "Öğrencinin doğum günü hangisidir?":
        Select(driver.find_element(By.ID, "ddlS1C1")).select_by_visible_text(birthday)

    if firstQuestion.text == "Öğrencinin doğum ayı hangisidir?":
        Select(driver.find_element(By.ID, "ddlS1C1")).select_by_visible_text(birthmonth)

    if firstQuestion.text == "Öğrencinin okuduğu şube hangisidir?":
        Select(driver.find_element(By.ID, "ddlS1C1")).select_by_visible_text(className)

    if firstQuestion.text == "Öğrencinin nüfusa kayıtlı olduğu ilçe hangisidir?":
        Select(driver.find_element(By.ID, "ddlS1C1")).select_by_visible_text(
            birthDistrict
        )

    if firstQuestion.text == "Öğrencinin nüfusa kayıtlı olduğu il hangisidir?":
        Select(driver.find_element(By.ID, "ddlS1C1")).select_by_visible_text(
            birthCounty
        )

    if secondtQuestion.text == "Öğrencinin doğum yılı nedir?":
        driver.find_element(By.ID, "txtS2T1").send_keys(birthyear)

    if secondtQuestion.text == "Öğrencinin doğum günü hangisidir?":
        Select(driver.find_element(By.ID, "ddlS2C1")).select_by_visible_text(birthday)

    if secondtQuestion.text == "Öğrencinin doğum ayı hangisidir?":
        Select(driver.find_element(By.ID, "ddlS2C1")).select_by_visible_text(birthmonth)

    if secondtQuestion.text == "Öğrencinin okuduğu şube hangisidir?":
        Select(driver.find_element(By.ID, "ddlS2C1")).select_by_visible_text(className)

    if secondtQuestion.text == "Öğrencinin nüfusa kayıtlı olduğu ilçe hangisidir?":
        Select(driver.find_element(By.ID, "ddlS2C1")).select_by_visible_text(
            birthDistrict
        )

    if secondtQuestion.text == "Öğrencinin nüfusa kayıtlı olduğu il hangisidir?":
        Select(driver.find_element(By.ID, "ddlS2C1")).select_by_visible_text(
            birthCounty
        )

    org = Image.open("original.png")
    org = org.resize((128, 128), Image.ANTIALIAS)
    for imageID in ["imgR1", "imgR2", "imgR3", "imgR4", "imgR5"]:
        userPicture = driver.find_element(By.ID, imageID)

        blur = Image.open(BytesIO(userPicture.screenshot_as_png))
        blur = blur.resize((128, 128), Image.ANTIALIAS)

        value = compare_ssim(org, blur, GPU=False)
        if value > 0.7:
            userPicture.click()
            break

    driver.find_element(By.ID, "btnTamam").click()

    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='İl Kontenjan İşlemleri']"))
    )

    driver.find_element(By.XPATH, "//a[@title='İl Kontenjan İşlemleri']").click()

    driver.execute_script(
        "arguments[0].scrollIntoView();", driver.find_element(By.ID, "pnlNotBilgisi")
    )

    driver.save_screenshot("notlar.png")

    print("saved")


finally:
    driver.quit()
