from LabelingModule import ModifyLabels
from tkinter import filedialog
from pathlib import Path

status = False

if __name__ == "__main__":

    while not status:
        directory = filedialog.askdirectory(title='Select Video')

        if len(directory) == 0:
            break

        path = Path(directory)
        path_data = path.parent
        folder_name = path.name

        status = ModifyLabels(path_data, folder_name)
