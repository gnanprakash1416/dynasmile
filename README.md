⭐ Star Dynasmile on GitHub — it motivates us a lot!

[![Share](https://img.shields.io/badge/share-000000?logo=x&logoColor=white)](https://x.com/intent/tweet?text=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/Abblix/Oidc.Server%20%23OpenIDConnect%20%23Security%20%23Authentication)
[![Share](https://img.shields.io/badge/share-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/Abblix/Oidc.Server)
[![Share](https://img.shields.io/badge/share-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/Abblix/Oidc.Server)
[![Share](https://img.shields.io/badge/share-FF4500?logo=reddit&logoColor=white)](https://www.reddit.com/submit?title=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/Abblix/Oidc.Server)
[![Share](https://img.shields.io/badge/share-0088CC?logo=telegram&logoColor=white)](https://t.me/share/url?url=https://github.com/Abblix/Oidc.Server&text=Check%20out%20this%20project%20on%20GitHub)

## Table of Contents
- [About](#-about)
- [Functionality](#-functionality)
- [How to Install](#-how-to-install)
- [Documentation](#-documentation)
- [Feedback and Contributions](#-feedback-and-contributions)
- [License](#-license)
- [Contacts](#%EF%B8%8F-contacts)

## 🚀 About

**Dynasmile** is a Python-based AI-driven dynamic smile analysis tool for dental research. It uses computer vision techniques to analyze smile process. As a dental application, it features:

- **Smile intensity estimation**: Dynasmile automatically analyzes the smile intensity across different frames of the video. It plots the smile intensity, which helps the dentist to locate the frame where the smile reaches its peak.

- **Landmark detecion and display**: Dynasmile detects dentofacial landmarks on patients fraces and overlays the result to the selected frame, providing a user-friendly interface for dental specialists.

- **Low cost**:Dynasmile do not rely on local graphical card. The special architecture of this software relies on EC2 server, which can be rent at low cost and used at any time.

## 🎓 Functionality

Dynasmile processes the video uploaded by the user. It conducts detailed smile analysis on the selected frame, which includes the detecion of 13 dentofacial landmarks and perform 9 measurements.

For convenience, the certification information is provided in the tables below:

### Dentofacial landmarks
|Number|Landmark name|
|:-|:-|
|1|Subnasale|
|2|Inferior upper lip border|
|3|Superior lower lip border|
|4|Right outer canthus|
|5|Left outer canthus| 
|6|Right outer smile commissure|
|7|Left outer smile sommissure|
|8|Soft tissue nasion|
|9|Soft tissue pogonion|
|10|Incisor edge| 
|11|Left upper cuspid tip|
|12|Right upper cuspid tip|
|13|Cervical part of incisor| 
|**total 13 landmarks**|

### Smile measurements
|Number|Measurement name|
|:-|:-|
|1|Intercommissure width|
|2|Interlabial gap|
|3|Gingival display|
|4|Philtrum height|
|5|Transverse symmetry| 
|6|Vertical symmetry|
|7|Dental angulation|
|8|Canthus and smile commissure deviation|
|**total 9 measurements**|


## 📝 How to Install

To build the packages, follow these steps:

```shell
# Open a terminal (Command Prompt or PowerShell for Windows, Terminal for macOS or Linux)

# Ensure Git is installed
# Visit https://git-scm.com to download and install console Git if not already installed

# Create a Amazon account, and create an Amazon EC2 instance with g4dn.xlarge
# For people who do this, you might have difficulties. Please feel free to contact dentistfrankchen@outlook.com

# Clone the repository to local computer
git clone https://github.com/dentistfrankchen/dynasmile.git

# Navigate to the project directory
cd The/path/to/your/project/directory

# Copy Amazon pem file to the ./client folder
# Make sure the python version of your computer is python==3.8.x
# Create python environment
python -m venv ./venv

# Install the requirements for the local interface.
./venv/Scripts/pip.exe install -r ./client/requirements.txt

# Install web service to the web server
python ./install_tools/install_service.py

```
## 📚 Documentation 

### Starting the program
```shell
# Open a terminal (Command Prompt or PowerShell for Windows, Terminal for macOS or Linux)

# Navigate to the project directory
cd The/path/to/your/project/directory

# Use the python program in venv folder to run the server-configuration.py
./venv/Scripts/python.exe ./client/server-configuration.py

# After the web service has been provoked, you can start the main interface.
./venv/Scripts/python.exe ./client/software/main.py

```

### Running the program to conduct smile analysis
1. Upload a video by clicking **'import_media' button**.
2. The program then uploads the video, displaying the process through the **progress bar**.
3. When the progress bar reaches 100 percent, the video will be automatically played.
4. Users can view the commissure.png in the project directory to click the **'pause' button** choose the where to pause to conduct the measurements and display the landmarks.
5. The user hits the **'load_from_algo' button** to render the landmarks. The measurements will be calculated and the same time.
6. The user clicks the **'save_to_csv'** button, and the coordinates of the landmarks as well as the measurements will be saved in CSV files.

## 🤝 Feedback and Contributions

We've made a lot of effort to implement many aspects of dynamic smile analysis in this software. However, the development journey doesn't end now, and your feedback is crucial for our further improvement.

> [!IMPORTANT]
> Whether you have feedback on improvements, have encountered any bugs, or have suggestions for features, we're cannot wait to hear from you. Your insights help us get our software more robust and user-friendly.

Please feel free to contribute by [submitting an issue](https://github.com/dentistfrankchen/dynasmile/issues). Each contribution helps us get better and improve.

We appreciate your kindly support and look forward to build our product even better with your help!

## 📃 License

This product is distributed under Apache license.

For non-commercial use, this product is available for free.

## 🗨️ Contacts

For more details about our products, services, or any general information regarding the Amazon EC2 server, feel free to contact us. We are here to provide needed support and answer any questions you have. Below are the best ways to contact our team:

- **Email**: Send us your inquiries or support requests at [dentistfrankchen@outlook.com](mailto:dentistfrankchen@outlook.com).


We look forward to assisting you and keeping your experience with our applicaion being enjoyable!

[Back to top](#top)
