import time
import re
import json

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ChromeOptions


class App:
    def __init__(self):
        pass

    def recorder(self):
        script = """
        document.onclick = function(event) {
            if (event === undefined) event = window.event;  // IE hack
            var target= 'target' in event? event.target : event.srcElement; // another IE hack

            var root = document.compatMode === 'CSS1Compat' ? document.documentElement : document.body;
            var mxy = [event.clientX + root.scrollLeft, event.clientY + root.scrollTop];

            var path = getPathTo(target);
            console.log(`action: click, target: ${path}, value: `)
        }

        document.onkeypress = function(evt) {
            evt = evt || window.event;
            var target = 'target' in evt? evt.target : evt.srcElement; // another IE hack
            var charCode = evt.keyCode || evt.which;
            var charStr = String.fromCharCode(charCode);    
            var element = getPathTo(target)   
            console.log(`action: type, target: ${element}, value: ${charStr}`) 
        };

        function getPathTo(element) {
            if (element.id !== '')
                return '//*[@id="'+element.id+'"]';
            if (element === document.body)
                return element.tagName;

            var ix = 0;
            var siblings = element.parentNode.childNodes;
            
            for (var i=0; i < siblings.length; i++) {
                var sibling= siblings[i];
                if (sibling === element)
                    return getPathTo(element.parentNode) + '/' + element.tagName + '['+(ix+1)+']';
                if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                    ix++;
            }
        }"""

        opts = ChromeOptions()
        d = DesiredCapabilities.CHROME
        d["goog:loggingPrefs"] = {"browser": "ALL"}

        driver = webdriver.Chrome(desired_capabilities=d, options=opts)

        driver.get("https://www.python.org/")
        driver.execute_script(script)

        for i in range(1, 5):
            print(i)
            time.sleep(1)

        regex_group = {"recorder": []}
        last_regex = dict()

        for index, entry in enumerate(driver.get_log("browser")):
            if "action" in entry["message"] and entry is not None:
                try:
                    matched_regex = list(
                        re.finditer(
                            '"\w+:\s(?P<action>\w+),\s\w+:\s(?P<target>(.*)(?=,)),\s\w+:\s(?P<value>(.*)(?="))',
                            entry["message"],
                        )
                    )[0].groupdict()

                    if (
                        index > 1
                        and matched_regex["target"] == last_regex.get("target")
                        and matched_regex["action"] == "type"
                    ):
                        regex_group["recorder"][-1]["action"] = "type"
                        regex_group["recorder"][-1]["value"] += matched_regex["value"]
                    else:
                        matched_regex["target"] = matched_regex["target"].replace("\\")
                        regex_group["recorder"].append(matched_regex)

                    last_regex = matched_regex

                except Exception as error:
                    print("Error: ", error)

        with open("result.json", "w") as json_file:
            json.dump(regex_group, json_file)

        driver.quit()

    def run(self):
        driver = webdriver.Chrome()
        driver.get("https://www.python.org/")

        with open("result.json") as json_file:
            data = json.load(json_file)

        selenium_methods = {
            "type": "send_keys",
            # "Combobox": "select_by_value",
            "click": "click",
        }
        for item in data["recorder"]:
            target = item["target"].replace("\\", "")
            element = driver.find_element_by_xpath(target)

            getattr(element, str(selenium_methods[item["action"]]))(
                item["value"]
            ) if item["action"] != "click" else getattr(
                element, str(selenium_methods[item["action"]])
            )()
