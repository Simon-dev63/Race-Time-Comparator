[README.md](https://github.com/user-attachments/files/24676551/README.md)
# 🏃 Race Time Comparator

**An open-source tool for Track and Cross-Country runners to benchmark their performance against the international pool.**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Built%20With-Python%20%7C%20Tkinter-blue)

## 📖 Overview
The **Race Time Comparator** is a desktop GUI application designed for runners of all ages (10-50). By inputting your age, sex, and race time, the tool generates a statistical frequency distribution (bell curve) simulating the international pool of runners for your specific demographic.

It visualizes exactly where you stand in the pack—whether you are in the top percentile or the middle of the curve.

## 🚀 Features
* **Demographic Specifics:** Adjustable inputs for Age (10-50) and Sex (Male/Female).
* **Event Variety:** * **Track:** 100m, 200m, 400m, 800m, 1600m, 3200m.
    * **Cross Country:** 1 Mile, 2 Miles, 3 Miles.
* **Visual Data:** Generates a real-time histogram using World Record baselines and Age-Graded statistics to simulate a realistic runner pool.
* **User Tracking:** Includes a live counter showing how many runners worldwide have used the tool.

## 📥 How to Use (Windows)
You do not need to install Python to use this tool.

1.  Navigate to the **[Releases]** section of this repository (or look in the root folder).
2.  Download `race_time.exe`.
3.  Double-click to run.
4.  Enter your details and click **Compare My Score**.

## 🛠️ For Developers: Running from Source
If you wish to modify the code or build it yourself:

### 1. Requirements
* Python 3.8+
* Pip

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone [https://github.com/YOUR_USERNAME/GlobalRaceComparator.git](https://github.com/YOUR_USERNAME/GlobalRaceComparator.git)
cd GlobalRaceComparator/src
pip install matplotlib numpy requests
