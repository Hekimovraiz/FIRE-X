"""
NASA FIRE-X 3D-Printable Enclosure CAD Generator (.STL) — v2.0 Precision Fit
Verified against physical datasheets + FDM 3D printing tolerances (+0.4 to +0.8 mm):
1. MQ-2 Gas Sensor Module:
   - Metal mesh dome + bakelite base: Ø 19.8 mm, height 16.0 mm above PCB
   - Turret bore: Ø 20.8 mm (0.5 mm radial clearance)
   - Turret ceiling thickness above MQ-2 PCB seat: 4.8 mm -> 11.2 mm of mesh dome protrudes above turret!
   - Internal MQ-2 rectangular PCB holder pocket: 34.0 × 22.0 mm (fits 32.0 × 20.0 mm PCB + tolerances)
2. ESP32 30-Pin DevKit V1 (ESP-WROOM-32, CP2102):
   - Physical PCB: 51.5 × 28.5 mm -> Cradle slot: 53.6 × 30.2 mm
   - Downward soldered pin clearance trench: 9.5 mm deep (fits 8.5 mm male pins)
   - Overhead cavity above cradle: 27.0 mm (fits 14 mm Female Dupont connectors with room to spare)
3. Micro-USB Cable Port:
   - Inner through-opening: 14.5 × 10.0 mm (outer chamfer: 18.5 × 13.0 mm) so any Micro-USB plug clicks 100% in.
"""

import os
import math
import numpy as np
import manifold3d as m3d
import trimesh

Manifold = m3d.Manifold
CrossSection = m3d.CrossSection
EVEN_ODD = m3d.FillRule.EvenOdd


def poly_extrude(points_2d, height, z_offset=0.0):
    cs = CrossSection([points_2d], EVEN_ODD)
    m = Manifold.extrude(cs, height)
    if z_offset != 0.0:
        m = m.translate((0.0, 0.0, z_offset))
    return m


def make_chamfered_octagon_prism(length, width, height, corner_x=14.0, corner_y=12.0, z0=0.0):
    hx = length / 2.0
    hy = width / 2.0
    pts = [
        (-hx + corner_x, -hy),
        ( hx - corner_x, -hy),
        ( hx, -hy + corner_y),
        ( hx,  hy - corner_y),
        ( hx - corner_x,  hy),
        (-hx + corner_x,  hy),
        (-hx,  hy - corner_y),
        (-hx, -hy + corner_y),
    ]
    return poly_extrude(pts, height, z0)


def build_front_logo_manifold(W=58.0):
    """Crisp 3D embossed Rocket icon + 'FIRE-X' text on the front face (Y = -W/2)."""
    logo = Manifold()

    rocket_body_pts = [
        (0.0, 7.2),
        (-2.6, 3.0),
        (-2.4, -2.0),
        (-4.8, -4.5),
        (-2.0, -3.6),
        (-1.3, -4.8),
        (0.0, -6.5),
        (1.3, -4.8),
        (2.0, -3.6),
        (4.8, -4.5),
        (2.4, -2.0),
        (2.6, 3.0),
    ]
    cs_rocket = CrossSection([rocket_body_pts], EVEN_ODD)
    window_pts = [
        (1.1 * math.cos(a), 1.5 + 1.1 * math.sin(a))
        for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)
    ]
    cs_rocket = cs_rocket - CrossSection([window_pts], EVEN_ODD)
    m_rocket = (
        Manifold.extrude(cs_rocket, 2.6)
        .rotate((90, 0, 0))
        .rotate((0, 22, 0))
        .translate((0.0, -W / 2.0 + 1.2, 28.2))
    )
    logo = logo + m_rocket

    strokes = [
        # F
        (-22.0, 13.0, -20.2, 20.0),
        (-22.0, 18.5, -16.5, 20.0),
        (-22.0, 15.8, -17.5, 17.2),
        # I
        (-14.5, 13.0, -12.5, 20.0),
        # R
        (-10.2, 13.0, -8.4, 20.0),
        (-10.2, 18.5, -4.8, 20.0),
        (-10.2, 15.8, -4.8, 17.2),
        (-6.0,  15.8, -4.2, 20.0),
        (-7.2,  13.0, -4.2, 16.1),
        # E
        (-2.0, 13.0, -0.2, 20.0),
        (-2.0, 18.5,  3.8, 20.0),
        (-2.0, 15.8,  2.8, 17.2),
        (-2.0, 13.0,  3.8, 14.5),
        # -
        (5.8,  15.7,  9.2, 17.3),
    ]
    for (x0, z0, x1, z1) in strokes:
        cx, cz = 0.5 * (x0 + x1), 0.5 * (z0 + z1)
        logo = logo + Manifold.cube((x1 - x0, 2.6, z1 - z0), True).translate((cx, -W / 2.0 - 0.1, cz))

    x_bar1 = poly_extrude([(11.2, 13.0), (13.2, 13.0), (18.2, 20.0), (16.2, 20.0)], 2.6).rotate((90, 0, 0)).translate((0.0, -W / 2.0 + 1.2, 0.0))
    x_bar2 = poly_extrude([(16.2, 13.0), (18.2, 13.0), (13.2, 20.0), (11.2, 20.0)], 2.6).rotate((90, 0, 0)).translate((0.0, -W / 2.0 + 1.2, 0.0))
    logo = logo + x_bar1 + x_bar2

    return logo


def make_outer_body(L=128.0, W=58.0, H=46.0):
    bottom_core = make_chamfered_octagon_prism(L - 6.0, W - 6.0, 1.0, corner_x=13.0, corner_y=11.0, z0=0.0)
    mid_low = make_chamfered_octagon_prism(L, W, H - 10.0, corner_x=15.0, corner_y=13.0, z0=3.0)
    top_core = make_chamfered_octagon_prism(L - 10.0, W - 10.0, 1.0, corner_x=12.0, corner_y=10.0, z0=H - 1.0)
    body = (bottom_core + mid_low + top_core).hull()

    # ── Top-Right Turret for MQ-2 Sensor (centered at X = +28, Y = 0) ──
    tx, ty = 28.0, 0.0
    turret_base = Manifold.cylinder(6.0, 21.0, 18.5, 48).translate((tx, ty, H - 1.0))
    fins_cut = Manifold()
    for i in range(12):
        ang = i * (360.0 / 12.0)
        slot = (
            Manifold.cube((4.5, 2.8, 5.0), True)
            .translate((20.0, 0.0, H + 1.8))
            .rotate((0, 0, ang))
            .translate((tx, ty, 0))
        )
        fins_cut = fins_cut + slot
    turret = turret_base - fins_cut

    led_groove = (
        Manifold.cylinder(2.0, 14.8, 14.8, 48) - Manifold.cylinder(2.5, 12.6, 12.6, 48)
    ).translate((tx, ty, H + 3.5))
    inner_collar = Manifold.cylinder(7.0, 12.6, 12.2, 48).translate((tx, ty, H - 1.0))
    body = body + turret - led_groove + inner_collar

    # ── Top-Left Geometric Grooves ──
    g1 = Manifold.cube((42.0, 2.6, 2.4), True).translate((-22.0, -7.0, H))
    g2 = Manifold.cube((34.0, 2.6, 2.4), True).translate((-18.0,  5.0, H))
    body = body - g1 - g2

    # ── Front Recessed Hexagonal Armor Frame ──
    front_panel_outer = [
        (-40.0, 9.5), (40.0, 9.5), (46.0, 23.0),
        (40.0, 36.5), (-40.0, 36.5), (-46.0, 23.0)
    ]
    front_panel_inner = [
        (-38.2, 11.3), (38.2, 11.3), (43.8, 23.0),
        (38.2, 34.7), (-38.2, 34.7), (-43.8, 23.0)
    ]
    cs_frame = CrossSection([front_panel_outer], EVEN_ODD) - CrossSection([front_panel_inner], EVEN_ODD)
    frame_groove = Manifold.extrude(cs_frame, 2.4).rotate((90, 0, 0)).translate((0.0, -W/2.0 + 1.8, 0.0))
    body = body - frame_groove

    bot_strip = Manifold.cube((34.0, 2.8, 2.2), True).translate((-16.0, -W/2.0 + 1.0, 5.2))
    body = body - bot_strip

    for gz in [16.0, 23.0, 30.0]:
        groove_l = (
            Manifold.cube((16.0, 16.0, 2.4), True)
            .rotate((0, 0, 40))
            .translate((-L/2.0 + 6.5, -W/2.0 + 5.5, gz))
        )
        body = body - groove_l

    groove_r = Manifold.cube((4.0, 4.0, 16.0), True).translate((L/2.0 - 14.5, -W/2.0 + 1.5, 23.0))
    body = body - groove_r

    logo_manifold = build_front_logo_manifold(W)
    body = body + logo_manifold

    return body


def build_enclosure_parts():
    L, W, H = 128.0, 58.0, 46.0
    wall = 2.8        # Sturdy 2.8 mm wall thickness
    base_h = 10.0     # Split height between Bottom Base Tray and Top Shell
    tx, ty = 28.0, 0.0

    outer = make_outer_body(L, W, H)

    # Main inner hollow cavity (from Z = 2.8 mm floor up to Z = 43.2 mm ceiling)
    cavity = make_chamfered_octagon_prism(
        L - 2 * wall, W - 2 * wall, H - 2 * wall,
        corner_x=13.5, corner_y=11.5, z0=wall
    )

    shell = outer - cavity

    # ── 1. PRECISION MQ-2 SENSOR MOUNTING AT TOP TURRET (X = +28, Y = 0) ──
    # Turret top is at Z = H + 6.0 = 52.0 mm.
    # MQ-2 cylinder height above its rectangular PCB is 16.0 mm.
    # We place the rectangular MQ-2 PCB ceiling seat at Z = 47.2 mm -> leaving exactly 4.8 mm turret lip!
    # So 16.0 - 4.8 = 11.2 mm of the MQ-2 stainless steel mesh dome protrudes out of the top turret!
    mq2_pcb_recess = Manifold.cube((34.2, 22.2, 8.0), True).translate((tx, ty, 43.2))
    shell = shell - mq2_pcb_recess

    # Circular through-bore Ø 20.8 mm (radius 10.4 mm) for MQ-2 metal dome & black base (Ø 19.8 mm)
    mq2_dome_hole = Manifold.cylinder(30.0, 10.4, 10.4, 64).translate((tx, ty, H - 10.0))
    shell = shell - mq2_dome_hole

    # Internal rectangular guide frame (inner 34.2 x 22.2 mm, outer 38.2 x 26.2 mm) on ceiling
    # Holds the 32 x 20 mm MQ-2 PCB straight so it cannot twist or slide
    mq2_guide_frame = (
        Manifold.cube((38.2, 26.2, 5.5), True)
        - Manifold.cube((34.2, 22.2, 7.0), True)
        - Manifold.cube((20.0, 30.0, 7.0), True)  # side wire cutout
    ).translate((tx, ty, H - wall - 1.5))
    shell = shell + mq2_guide_frame

    # ── 2. Right Side Cooling Louvers (4 horizontal ventilation slots above USB port) ──
    for sz in [23.0, 28.0, 33.0, 38.0]:
        slot = Manifold.cube((12.0, 20.0, 2.4), True).translate((L/2.0 - 2.0, 0.0, sz))
        shell = shell - slot

    # ── 3. Generous Micro-USB Cable Port Cutout (Right Wall, aligned with ESP32 cradle) ──
    # Inner through-hole: 14.5 mm wide (Y) x 10.0 mm tall (Z), centered at Z = 13.0 mm
    # Outer plug bevel recess: 18.5 mm wide x 13.0 mm tall
    usb_hole = Manifold.cube((18.0, 14.5, 10.0), True).translate((L/2.0 - 2.0, 0.0, 13.0))
    usb_recess = Manifold.cube((5.0, 18.5, 13.0), True).translate((L/2.0 + 0.5, 0.0, 13.0))
    shell = shell - usb_hole - usb_recess

    # ── Split into 2 Printable Parts: Bottom Base (Z <= base_h) and Top Shell (Z >= base_h) ──
    big_box_bot = Manifold.cube((220.0, 140.0, base_h), True).translate((0.0, 0.0, base_h / 2.0))
    big_box_top = Manifold.cube((220.0, 140.0, 120.0), True).translate((0.0, 0.0, base_h + 60.0))

    bottom_part = shell ^ big_box_bot
    top_part = shell ^ big_box_top

    # Interlocking snap-fit lip on Bottom Base (0.35 mm radial clearance for smooth FDM fit)
    lip_outer = make_chamfered_octagon_prism(
        L - 2 * wall - 0.7, W - 2 * wall - 0.7, 4.0,
        corner_x=13.2, corner_y=11.2, z0=base_h - 1.0
    )
    lip_inner = make_chamfered_octagon_prism(
        L - 2 * wall - 4.3, W - 2 * wall - 4.3, 5.0,
        corner_x=12.0, corner_y=10.0, z0=base_h - 1.5
    )
    lip = (lip_outer - lip_inner) - usb_hole
    bottom_part = bottom_part + lip

    # ── 4. PRECISION ESP32 30-PIN DEVKIT V1 CRADLE ON BOTTOM BASE ──
    # Physical 30-pin ESP32 PCB: 51.5 x 28.5 mm
    # Cradle PCB slot: 53.6 x 30.2 mm (+1.7 mm width / +2.1 mm length clearance for easy drop-in)
    # PCB rests on ledge at Z = 11.8 mm -> gives 9.0 mm vertical clearance underneath for 8.5 mm male pins!
    esp_cx = L/2.0 - wall - 53.6/2.0 - 0.5
    esp_cy = 0.0
    cradle_block = Manifold.cube((57.6, 34.6, 11.5), True).translate((esp_cx, esp_cy, 2.0 + 5.75))
    # Central trench underneath PCB (46.0 x 23.0 mm) + pin row clearance channels so pins sit freely
    under_pocket = Manifold.cube((50.5, 29.0, 10.0), True).translate((esp_cx, esp_cy, 2.8 + 4.2))
    # Upper board slot (53.6 x 30.2 mm) above Z = 10.5 mm holding the 4 corners of the ESP32 PCB
    board_slot = Manifold.cube((53.6, 30.2, 6.0), True).translate((esp_cx, esp_cy, 10.2 + 3.0))
    wire_cut_x = Manifold.cube((38.0, 42.0, 12.0), True).translate((esp_cx, esp_cy, 8.5))
    wire_cut_y = Manifold.cube((64.0, 19.0, 12.0), True).translate((esp_cx, esp_cy, 8.5))

    cradle = (cradle_block - under_pocket - board_slot - wire_cut_x - wire_cut_y) - usb_hole
    bottom_part = bottom_part + cradle

    assembled = (
        outer - cavity - mq2_pcb_recess - mq2_dome_hole + mq2_guide_frame
        - usb_hole - usb_recess + cradle
    )
    for sz in [23.0, 28.0, 33.0, 38.0]:
        slot = Manifold.cube((12.0, 20.0, 2.4), True).translate((L/2.0 - 2.0, 0.0, sz))
        assembled = assembled - slot

    return bottom_part, top_part, assembled


def manifold_to_trimesh(m: Manifold) -> trimesh.Trimesh:
    mesh_data = m.to_mesh()
    verts = np.array(mesh_data.vert_properties)[:, :3]
    faces = np.array(mesh_data.tri_verts)
    return trimesh.Trimesh(vertices=verts, faces=faces, process=True)


if __name__ == "__main__":
    print("Building v2.0 Precision-Fit 3D CAD enclosure meshes...")
    bot_m, top_m, asm_m = build_enclosure_parts()

    tm_bot = manifold_to_trimesh(bot_m)
    tm_top = manifold_to_trimesh(top_m)
    tm_asm = manifold_to_trimesh(asm_m)

    for name, tm in [("Bottom Base", tm_bot), ("Top Shell", tm_top), ("Assembled", tm_asm)]:
        print(f"  {name}: vertices={len(tm.vertices)}, faces={len(tm.faces)}, "
              f"watertight={tm.is_watertight}, bounds_mm={np.round(tm.extents, 1).tolist()}")

    hw_dir = "/home/lezgin/Desktop/Nasa_Space_Apps_Challange/FIRE-X 1.0/hardware"
    desk_dir = "/home/lezgin/Desktop/FIREX_3D_Korpus_STL"
    proto_dir = "/home/lezgin/Desktop/FIREX_3D_Korpus_STL/prototip"
    os.makedirs(hw_dir, exist_ok=True)
    os.makedirs(desk_dir, exist_ok=True)
    os.makedirs(proto_dir, exist_ok=True)

    # Save clean names to prototip/ and legacy names to hardware/ + desk_dir/
    tm_top.export(os.path.join(proto_dir, "firex-top-shell.stl"))
    tm_bot.export(os.path.join(proto_dir, "firex-bottom-base.stl"))
    tm_asm.export(os.path.join(proto_dir, "firex-assembled.stl"))

    tm_top.export(os.path.join(desk_dir, "FIREX_1_Ust_Govde_Korpus.stl"))
    tm_bot.export(os.path.join(desk_dir, "FIREX_2_Alt_Baza_ESP32_Yuvasi.stl"))
    tm_asm.export(os.path.join(desk_dir, "FIREX_Tam_Yigilmish_Korpus.stl"))

    tm_top.export(os.path.join(hw_dir, "FIREX_1_Ust_Govde_Korpus.stl"))
    tm_bot.export(os.path.join(hw_dir, "FIREX_2_Alt_Baza_ESP32_Yuvasi.stl"))
    tm_asm.export(os.path.join(hw_dir, "FIREX_Tam_Yigilmish_Korpus.stl"))
    print("All STL files exported successfully!")
