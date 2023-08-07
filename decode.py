import tkinter as tk
from tkinter import filedialog
import nbtlib
import os

def choose_schematic_file():
	root = tk.Tk()
	root.withdraw()
	file_path = filedialog.askopenfilename(filetypes=[("Schematic Files", "*.schem")])
	root.destroy()
	return file_path

def decode_schematic_to_nbt(schematic_file_path):
	nbt_file = nbtlib.load(schematic_file_path)

	return nbt_file

def create_mcfunction_file(file_name, blocks_with_coordinates, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Create the .mcfunction file in the "output" directory
    mcfunction_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_name))[0]}.mcfunction")

    with open(mcfunction_path, "w") as mcfunction_file:
        for block_info in blocks_with_coordinates:
            x, y, z = block_info['x'], block_info['y'], block_info['z']
            block_name = block_info['block_name']
            mcfunction_file.write(f"execute at @s run setblock ~{x} ~{y} ~{z} {block_name}\n")

    print(f"MCFunction file created: {mcfunction_path}")

def getChoords(nbt_data):
    print(nbt_data.keys())

    # Extract the relevant information
    palette = nbt_data['Palette']
    block_data = nbt_data['BlockData']
    offset = nbt_data['Offset']

    # Create a list to store the extracted blocks and their coordinates
    blocks_with_coordinates = []

    # Find the minimum x, y, and z values
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')

    # Iterate through the block data to find the minimum values
    for index, block_id in enumerate(block_data):
        x = index % nbt_data['Width'] + offset[0]
        y = (index // (nbt_data['Width'] * nbt_data['Length'])) % nbt_data['Height'] + offset[1]
        z = (index // nbt_data['Width']) % nbt_data['Length'] + offset[2]
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)

    # Adjust coordinates relative to the minimum values
    for index, block_id in enumerate(block_data):
        x = index % nbt_data['Width'] + offset[0] - min_x
        y = (index // (nbt_data['Width'] * nbt_data['Length'])) % nbt_data['Height'] + offset[1] - min_y
        z = (index // nbt_data['Width']) % nbt_data['Length'] + offset[2] - min_z
        block_name = next(key for key, value in palette.items() if value == block_id)
        blocks_with_coordinates.append({'block_name': block_name, 'x': x, 'y': y, 'z': z})
        
    return blocks_with_coordinates


# Usage example with Tkinter file dialog:
schematic_path = choose_schematic_file()

if schematic_path:
	nbt_data = decode_schematic_to_nbt(schematic_path)
	if nbt_data:
		# Do something with the nbt_data here
		print("Schematic file decoded successfully.")
		blocks_with_coordinates = getChoords(nbt_data)
		current_directory = os.path.dirname(os.path.abspath(__file__))
		output_directory = os.path.join(current_directory, "output")
		create_mcfunction_file(schematic_path, blocks_with_coordinates, output_directory)
else:
	print("No file selected or invalid file.")
