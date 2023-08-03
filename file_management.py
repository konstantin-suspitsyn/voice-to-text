import os
import yaml


class FileManager:
    """
    Helper function for voice-to-text

    Checks for files and folders
    """
    INPUT_PATHS_KEY = "input_paths"
    OUTPUT_PATH_KEY = "output_folder"
    PATHS_YML = "file_paths.yml"

    def __init__(self):
        with open(self.PATHS_YML, 'r') as stream:
            self.file_list: dict = yaml.safe_load(stream)
        self.__check_errors_in_file_paths()
        self.__create_folder_if_not_exists()

    def get_list_of_files(self) -> dict:
        """
        :return: dictionary with file
        """
        return self.file_list

    def are_files_exist(self) -> bool:
        for file_path in self.file_list[self.INPUT_PATHS_KEY]:
            if not os.path.isfile(file_path):
                return False
        return True

    def __check_for_keys_in_file_paths_dictionary(self, key: str) -> None:
        if key not in self.file_list:
            raise KeyError(f"{key} should be in {self.PATHS_YML} file. You can find more info "
                           f"about {self.PATHS_YML} in README.md")

    def __check_errors_in_file_paths(self) -> None:
        self.__check_for_keys_in_file_paths_dictionary(self.INPUT_PATHS_KEY)
        self.__check_for_keys_in_file_paths_dictionary(self.OUTPUT_PATH_KEY)

        if type(self.file_list[self.INPUT_PATHS_KEY]) != list:
            raise TypeError(f"Input file paths should be list. Even if you have one file. More info in README.md")

        if type(self.file_list[self.OUTPUT_PATH_KEY]) != str:
            raise TypeError(f"Output folder path should be one string. More info in README.md")

    def __create_folder_if_not_exists(self):
        if not os.path.exists(self.file_list[self.OUTPUT_PATH_KEY]):
            os.mkdir(self.file_list[self.OUTPUT_PATH_KEY])
