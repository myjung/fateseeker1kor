from dataclasses import dataclass
import toml as tomllib
import pathlib
from shutil import copyfile
import csv
import io

import UnityPy
from UnityPy.enums import ClassIDType


@dataclass
class FateSeeker1MetaInfo:
    # textfiles
    localization = "assets/forassetbundles/textfiles/localization.csv"
    # movie_other
    opening = "assets/forassetbundles/movies/other/opening_chinese.bytes"
    dlc_opening = "assets/forassetbundles/movies/other/dlcopening_chinese.bytes"


class FateSeeker1Patcher:
    @staticmethod
    def backup_asset(
        setting_path: pathlib.Path, target_path=pathlib.Path("./extracted_assets")
    ) -> None:
        settings = tomllib.load(setting_path)["local"]
        game_path = pathlib.Path(settings["GAME_PATH"])
        asset_path = game_path.joinpath(
            "FateSeeker/FateSeeker_Data/StreamingAssets/StandaloneWindows64"
        )
        text_files = asset_path.joinpath("textfiles")
        movie_other = asset_path.joinpath("movie_other")
        copyfile(text_files, target_path.joinpath("textfiles.bak"))
        copyfile(movie_other, target_path.joinpath("movie_other.bak"))

    def __init__(self, extracted_asset_path: pathlib.Path) -> None:
        # copy assets from backupfiles and Load
        copyfile(
            extracted_asset_path.joinpath("textfiles.bak"),
            extracted_asset_path.joinpath("textfiles"),
        )
        copyfile(
            extracted_asset_path.joinpath("movie_other.bak"),
            extracted_asset_path.joinpath("movie_other"),
        )
        self.textfiles = UnityPy.load(str(extracted_asset_path.joinpath("textfiles")))
        self.movie_other = UnityPy.load(
            str(extracted_asset_path.joinpath("movie_other"))
        )

    def get_text(self, path: str) -> str:
        asset = self.textfiles.container[path]
        if not asset.type == ClassIDType.TextAsset:
            raise Exception("Not Text Asset")
        t = ""
        try:
            t = asset.read().text
        except UnicodeDecodeError:
            t = bytes(asset.read().script).decode("big5hkscs")
        if t[:1] == "\ufeff":
            return t[1:]
        else:
            return t

    def set_text(self, path: str, text: str) -> None:
        asset = self.textfiles.container[path]
        if not asset.type == ClassIDType.TextAsset:
            raise Exception("Not Text Asset")
        data = asset.read()
        data.script = text.encode("utf-8")
        data.save()

    def save_asset(self, path: str) -> None:
        with open(path, mode="wb") as f:
            f.write(self.textfiles.file.save())



class FateSeekerCsvParser:
    def __init__(self, text:str) -> None:
        self.text = text
    
    def change_by_key(self, key_translated:dict) -> list:
        output = io.StringIO()
        output.write(",".join(("Key","Chinese","China")))
        output.write("\r\n")
        for row in csv.DictReader(self.text.splitlines()):
            if row['Key'] in key_translated:
                row['Chinese'] = key_translated[row['Key']]
            output.write(f"{row['Key']},{row['Chinese']},{row['China']}\r\n")
        return output.getvalue()


class FateSeeker1PatchHelper:
    def __init__(self, patcher: FateSeeker1Patcher) -> None:
        self.patcher = patcher

    def extract_text(self) -> list:
        # extract text assets from asset files
        pass

    def patch(self, translated_csv: str, output_path: str) -> None:
        # replace text with translated text
        self.patcher.set_text("assets/forassetbundles/textfiles/localization.csv", translated_csv)
        pass


if __name__ == "__main__":
    current_file_path = pathlib.Path(__file__)
    local_config_path = current_file_path.parent.joinpath("..", "localconfig.toml")
    # ph = PatchHelper(PatchTargets, patcher)
    # ph.patch("translated2403082200.csv","config")
    # ph.extract_every_keywords_to_file("2403082000.csv")
