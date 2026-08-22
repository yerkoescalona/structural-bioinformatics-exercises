load 2IEN.pdb, prot
bg_color white
hide everything
show cartoon, prot and polymer
color skyblue, prot and chain A and polymer
color salmon, prot and chain B and polymer
show sticks, resn 017
color yellow, resn 017
util.cnc resn 017
set ray_opaque_background, 0
orient prot
ray 1200, 900
png 2IEN_render.png, dpi=150
print("RENDER_DONE")
