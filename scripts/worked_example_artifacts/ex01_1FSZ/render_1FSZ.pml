# PyMOL script — real headless render of the downloaded 1FSZ.pdb
# Confirms the structure is visualizable and shows chain/domain/GDP layout.
load 1FSZ.pdb, fsz
bg_color white
hide everything
show cartoon, fsz and polymer
color skyblue, fsz and polymer and resi 23-189
color salmon, fsz and polymer and resi 190-356
show sticks, resn GDP
color yellow, resn GDP
util.cnc resn GDP
set ray_opaque_background, 0
orient fsz
ray 1200, 900
png 1FSZ_render.png, dpi=150
print("RENDER_DONE")
