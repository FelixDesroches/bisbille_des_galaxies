import numpy as np
from pywavefront import Wavefront
from os.path import basename
from tqdm import tqdm

from src.engine.relative_paths import get_path


class MaterialLoader:
    """
    Note: for inconsistent vertex format, try searching for the characters // in the .obj and replacing it with /1/.
    """
    def __init__(self):
        self.object_materials = {}
        for obj, filename in [
            # ("millenium_falcon", "Star Wars FALCON centered.obj"),
            ("star_destroyer", "StarDestroyer.obj"),
            # ("tie_fighter", "processed_tie.obj"),
            # ("malevolence", "emship_hq.obj"),
            # ("corvette", "CR90_New.obj"),
            # ("royal_starship", "model.obj")
            # ("imperial_shuttle", "imperial_shuttle_ver1.obj"),
            # ("a_wing", "a_wing.obj"),
        ]:
            path = get_path(f"objects/{obj}")
            materials = []
            for material in Wavefront(f"{path}/{filename}", collect_faces=True, strict=False).materials.values():
                if material.vertices:
                    materials.append((material.name, material.vertices))
            self.object_materials[obj] = materials

    @staticmethod
    def recenter_obj_file(input_path, output_path):
        vertices = []
        with open(input_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("v "):
                parts = line.split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)

        vertices = np.array(vertices)
        center = np.mean(vertices, axis=0)

        with open(output_path, "w") as file:
            for line in lines:
                if line.startswith("v "):
                    parts = line.split()
                    vertex = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                    centered_vertex = vertex - center
                    file.write(f"v {centered_vertex[0]} {centered_vertex[1]} {centered_vertex[2]}\n")
                else:
                    file.write(line)

    @staticmethod
    def fix_invalid_vertex_format(input_path, output_path):
        with open(input_path, "r") as file:
            lines = file.readlines()

        new_lines = []

        for line in tqdm(lines, colour="green"):
            cropped_line = line.split("//")
            if len(cropped_line) > 1:
                new_lines.append("/1/".join(cropped_line))
            else:
                new_lines.append(line)

        with open(output_path, "w") as file:
            file.writelines(new_lines)

    @staticmethod
    def fix_index_out_of_range(input_path, output_path):
        with open(input_path, "r") as file:
            lines = file.readlines()

        new_lines = []

        for line in tqdm(lines, colour="MAGENTA"):
            new_line = []
            splitted_lines = line.split(" ")
            for split in splitted_lines:
                split_split = split.split("/")
                match len(split_split):
                    case 1 | 3:
                        new_line.append(split)
                    case 2:
                        new_line.append(f"{split_split[0]}/1/{split_split[1]}")
                    case _:
                        raise ValueError(f"Invalid vertex index: {split}")

            new_lines.append(" ".join(new_line))

        with open(output_path, "w") as file:
            file.writelines(new_lines)
