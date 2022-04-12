# Quick notes on Selenium

## Finding web elements

https://www.selenium.dev/documentation/webdriver/elements/finders/

1. By class name:

```py
from selenium.webdriver.common.by import By

vegetable = driver.find_element(By.CLASS_NAME, "tomatoes")
```

2. Find an element of an element

```py
fruits = driver.find_element(By.ID, "fruits")
fruit = fruits.find_elements_by_id("tomatoes")
```

3. By CSS selector

```py
fruit = driver.find_element_by_css_selector("#fruits .tomatoes")
```
