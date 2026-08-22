load 3D08.pdb, p53
bg_color white
hide everything
show cartoon, p53 and polymer
color gray80, p53 and polymer
show spheres, resn ZN
color purple, resn ZN
show sticks, resi 249 and polymer
color red, resi 249 and polymer
set ray_opaque_background, 0
orient p53
ray 1200, 900
png 3D08_render.png, dpi=150
print("RENDER_DONE")
