## 🌟 dynamic-selenium-recorder

This repo is a Python project that leverages the Selenium library to record and replay actions performed in the browser. The main script captures click and typing events in the browser, saving them to a local file named `actions.json`, enabling the automated execution of these actions at a later time.

### 🔧 Technologies Used
- **Python**: The primary language for automating actions in the browser.
- **Selenium**: Library used for automated interaction with the browser.
- **JavaScript**: Used to capture click and typing events in the browser.

### 🚀 Key Features
1. **Action Recording**: The script captures click and typing events in the browser, saving them in JSON format in the `actions.json` file.
   
2. **Automated Playback**: Allows for routine execution of recorded actions, facilitating the automation of repetitive tasks.

### 📝 Main Script Structure
- **Click Event Capture**: Utilizes click events to identify the target element and records the action in the `actions.json` file.
- **Typing Event Capture**: Records user typing, including the target element and the typed value.
- **Element Localization**: The `getPathTo(element)` method is used to obtain the XPath path of the target element in the browser.
  
### ℹ️ How to Use
1. Clone the repository to your local machine.
2. Install the necessary dependencies, including Selenium.
3. Run the main Python script to start recording actions.
4. The actions will be saved in the `actions.json` file.
5. To replay the actions, use the recorded file with the automated script.
