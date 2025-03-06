# YOLO-Image-Annotation-Tool
A lightweight YOLO image annotation tool for creating and editing bounding box annotations. Supports drawing, deleting, and classifying objects with an intuitive interface.


# YOLO Image Annotation Tool
A lightweight tool for creating and editing bounding box annotations in YOLO format. This tool allows you to efficiently label images with rectangular bounding boxes and assign classes to them, making it perfect for preparing training data for YOLO-based object detection models.

# Features
* **YOLO Format Compatible**: Creates annotation files in the format required by YOLO models.
* **Intuitive Interface**: Left-click to draw boxes, right-click to delete boxes, middle mouse button to define class.
* **Automatic File Handling**: Automatically reads and displays existing annotations, or creates new ones as needed.
* **Multiple Image Format Support**: Works with various image formats.
* **Organized Output**: Creates a dedicated Results folder in the same directory as your images folder.
* **Persistence**: Saves annotation data in text files compatible with YOLO frameworks.

# Installation
**Prerequisites**
    
* Python 3.6+
* Required Python packages:
```  
pip install opencv-python tkinter
```
**Setup**

**1.** Clone this repository:
```  
git clone https://github.com/yourusername/yolo-annotation-tool.git
```
**2.** Navigate to the repository directory:
```  
cd yolo-annotation-tool
```
**3.** Install dependencies:
```  
pip install opencv-python
```
Note: tkinter usually comes pre-installed with Python, but if not, you may need to install it separately.

# Usage

**1.** Run the main script:
```  
python main.py
```
**2.** When prompted, select the folder containing the images you want to annotate.

**3.** The tool will open and display the first image in the folder.

**Controls:**

- **Left Mouse Button**: Draw a bounding box.
- **Right Mouse Button**: Delete a selected bounding box.
- **Middle Mouse Button**: Define class for the currently selected box.
- **Ctrl+S**: Save current annotations.
- **Ctrl+N**: Skip image without saving.
- **Ctrl+F**: Select new folder.
- **Ctrl+Q**: Quit tool.

# File Format
Annotations are saved in YOLO format text files with the same name as their corresponding image file but with a .txt extension. Each line in the text file represents one bounding box in the format:
```  
<class_id> <x_center> <y_center> <width> <height>
```
where:
- class_id: Integer representing the class ID (0-indexed).
- x_center, y_center: Normalized coordinates (0-1) of the center of the bounding box.
- width, height: Normalized width and height of the bounding box (0-1).
