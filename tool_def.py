
def is_element_exist(xpath,browser):
	try:
		browser.find_element_by_xpath(xpath)
	except:
		return False
	else:
		return True

