import glob
import re
import os

script_name = os.path.basename(__file__)


def removing_unwanted_characters(text:str, all_dots: bool = True) -> str:
    """
    This function allows to remove all special characters from our unclean string.
    It removes all non-alphanummeric characters ... and replace then with the underscore character.
    :param text: input string that we want to clean
    :param all_dots: it allows to decide whether or not we want to remove all dots or all dots except the last one
    :return: clean text without any special character
    """
    flag = re.findall(r"[^a-zA-Z0-9\_]",filename)
    if flag:
        text =  re.sub('[^a-zA-Z0-9\.\_]', '_', text)

        if all:
            text = text.replace('.', '', text.count('.'))
        else:
            # replaces all dots except the last one
            text = text.replace('.', '', text.count('.') - 1)

    return text


print(f"Starting the script {script_name}")
for filename in glob.glob('*.*'):
    new_file_name =  removing_unwanted_characters(filename, all=False)
    if filename != new_file_name:
        os.rename(filename,new_file_name)
        print(f"I have just renamed a file from  called {filename} to {new_file_name}")

print(f"The end {script_name}")