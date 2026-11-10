"""
NASA FIRE-X 3D-Printable Enclosure CAD Generator (.STL) — v3.1 Coaxial Glueless Modular Edition
100% GLUELESS (Yapışqansız, Taxıb-Çıxarılan) — All components snap into the Bottom Base (Alt Baza):
1. Left Cradle (X = -33.6, Y = 0): ESP32 30-Pin DevKit V1 (53.2 × 29.6 mm slot + 4 corner clips
   + 9.5 mm under-board pin trench + Left-Wall USB port).
2. Center-Right Coaxial Pedestal Tower (X = +5.2 to +38.4, Y = -10.5 to +10.5):
   - Holds the asymmetric 32.0 × 20.0 mm MQ-2 PCB at Z = 34.0 mm so its Ø 19.8 mm metal mesh dome
     (centered 10.0 mm from the right edge of the PCB) sits at EXACTLY (X = +28.0, Y = 0.0),
     100% coaxial with the Top Cover's Ø 21.2 mm Turret bore!
   - The 4-pin header end of the MQ-2 PCB (X = +6.0) faces the ESP32 with an open 31 mm tall under-arch
     for the potentiometer and Female Dupont connectors.
3. Far-Right Acoustic Chamber (X = +50.0, Y = 0.0):
   - Ø 12.4 mm Active Buzzer friction-fit C-clip socket right beside the acoustic louvers.
4. Front/Rear Status LED Sockets (X = +1.0, Y = ±16.5):
   - 2× Ø 5.3 mm friction-fit sockets for 5mm Green & Red LEDs + top viewing ports.
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

    # ── 1. TOP TURRET PASS-THROUGH BORE (Ø 21.2 mm) SO TOP COVER LIFTS OFF FREELY ──
    mq2_dome_hole = Manifold.cylinder(30.0, 10.6, 10.6, 64).translate((tx, ty, H - 12.0))
    shell = shell - mq2_dome_hole

    # Dual 5mm LED top viewing ports at X = +1.0, Y = -16.5 and Y = +16.5
    led1_top_hole = Manifold.cylinder(12.0, 2.8, 2.8, 32).translate((1.0, -16.5, H - 6.0))
    led2_top_hole = Manifold.cylinder(12.0, 2.8, 2.8, 32).translate((1.0,  16.5, H - 6.0))
    shell = shell - led1_top_hole - led2_top_hole

    # ── 2. Acoustic & Cooling Louvers on Both Ends ──
    for sz in [23.0, 28.0, 33.0, 38.0]:
        slot_r = Manifold.cube((12.0, 20.0, 2.4), True).translate((L/2.0 - 2.0, 0.0, sz))
        slot_l = Manifold.cube((12.0, 20.0, 2.4), True).translate((-L/2.0 + 2.0, 0.0, sz))
        shell = shell - slot_r - slot_l

    # ── 3. USB Cable Port Cutouts (Left Wall for ESP32 + Right Wall auxiliary port) ──
    usb_hole_l = Manifold.cube((18.0, 14.5, 10.0), True).translate((-L/2.0 + 2.0, 0.0, 13.0))
    usb_recess_l = Manifold.cube((5.0, 18.5, 13.0), True).translate((-L/2.0 - 0.5, 0.0, 13.0))
    usb_hole_r = Manifold.cube((18.0, 14.5, 10.0), True).translate((L/2.0 - 2.0, 0.0, 13.0))
    usb_recess_r = Manifold.cube((5.0, 18.5, 13.0), True).translate((L/2.0 + 0.5, 0.0, 13.0))
    shell = shell - usb_hole_l - usb_recess_l - usb_hole_r - usb_recess_r

    # ── Split into 2 Printable Parts: Bottom Base (Z <= base_h) and Top Shell (Z >= base_h) ──
    big_box_bot = Manifold.cube((220.0, 140.0, base_h), True).translate((0.0, 0.0, base_h / 2.0))
    big_box_top = Manifold.cube((220.0, 140.0, 120.0), True).translate((0.0, 0.0, base_h + 60.0))

    bottom_part = shell ^ big_box_bot
    top_part = shell ^ big_box_top

    # Easy-open alignment lip on Bottom Base (0.45 mm radial clearance for smooth hand lift-off)
    lip_outer = make_chamfered_octagon_prism(
        L - 2 * wall - 0.9, W - 2 * wall - 0.9, 3.2,
        corner_x=13.2, corner_y=11.2, z0=base_h - 0.8
    )
    lip_inner = make_chamfered_octagon_prism(
        L - 2 * wall - 4.3, W - 2 * wall - 4.3, 4.5,
        corner_x=12.0, corner_y=10.0, z0=base_h - 1.2
    )
    lip = (lip_outer - lip_inner) - usb_hole_l - usb_hole_r
    bottom_part = bottom_part + lip

    # ══════════════════════════════════════════════════════════════════════════
    # 4. GLUELESS MODULAR COMPONENT CRADLES ON BOTTOM BASE (ALT BAZA)
    # ══════════════════════════════════════════════════════════════════════════

    # ── (A) LEFT CRADLE: ESP32 30-PIN DEVKIT V1 (X = -33.9, Y = 0.0) ──
    esp_cx = -L/2.0 + wall + 53.6/2.0 + 0.5  # X = -33.9 mm
    esp_cy = 0.0
    cradle_block = Manifold.cube((57.6, 34.4, 12.2), True).translate((esp_cx, esp_cy, 2.0 + 6.1))
    under_pocket = Manifold.cube((50.2, 28.6, 10.0), True).translate((esp_cx, esp_cy, 2.8 + 4.2))
    board_slot = Manifold.cube((53.0, 29.6, 6.5), True).translate((esp_cx, esp_cy, 10.2 + 3.25))
    wire_cut_x = Manifold.cube((34.0, 42.0, 13.0), True).translate((esp_cx, esp_cy, 8.8))
    wire_cut_y = Manifold.cube((64.0, 18.0, 13.0), True).translate((esp_cx, esp_cy, 8.8))
    esp_cradle = (cradle_block - under_pocket - board_slot - wire_cut_x - wire_cut_y) - usb_hole_l

    # ── (B) CENTER-RIGHT COAXIAL PEDESTAL TOWER FOR MQ-2 SENSOR (GLUELESS!) ──
    # Standard MQ-2 PCB is 32.0 mm long × 20.0 mm wide.
    # Its Ø 19.8 mm metal dome is centered 10.0 mm from the right edge of the PCB and 22.0 mm from the 4-pin left edge.
    # To keep the metal dome coaxial with the Top Turret at (tx = +28.0, ty = 0.0):
    # - PCB right edge sits at X = +28.0 + 10.4 = +38.4 mm
    # - PCB left (4-pin) edge sits at X = +28.0 - 22.4 = +5.6 mm
    # - PCB center is at p_cx = (+38.4 + 5.6) / 2 = +22.0 mm, p_cy = 0.0 mm!
    p_cx, p_cy = 22.0, 0.0
    tower_outer = Manifold.cube((37.6, 25.6, 36.7), True).translate((p_cx, p_cy, 2.8 + 36.7 / 2.0))
    # Upper PCB friction-fit pocket (Z = 34.0 to 40.0 mm): inner 32.8 × 20.8 mm
    pcb_pocket = Manifold.cube((32.8, 20.8, 7.0), True).translate((p_cx, p_cy, 34.0 + 3.5))
    # Under-PCB hollow chamber (Z = 2.8 to 34.0 mm): inner 29.2 × 17.6 mm (leaves 1.8 mm support ledge on all 4 sides)
    under_tower = Manifold.cube((29.2, 17.6, 32.0), True).translate((p_cx, p_cy, 2.8 + 16.0))
    # Wide arch cutouts on all 4 sides so the 4 MQ-2 pins, potentiometer, and Female Dupont wires pass freely
    arch_x = Manifold.cube((42.0, 12.6, 28.0), True).translate((p_cx, p_cy, 2.8 + 14.0))
    arch_y = Manifold.cube((20.0, 30.0, 28.0), True).translate((p_cx, p_cy, 2.8 + 14.0))
    # Finger grab cutouts on top walls so MQ-2 can be lifted out or pressed in by hand
    grip_slot_x = Manifold.cube((40.0, 10.0, 8.0), True).translate((p_cx, p_cy, 37.0))
    grip_slot_y = Manifold.cube((14.0, 28.0, 8.0), True).translate((p_cx, p_cy, 37.0))

    mq2_tower = (
        tower_outer - pcb_pocket - under_tower - arch_x - arch_y - grip_slot_x - grip_slot_y
    ) - usb_hole_r

    # ── (C) FAR-RIGHT SOCKET: 12MM ACTIVE BUZZER C-CLIP HOLDER (X = +50.0, Y = 0.0) ──
    buz_x, buz_y = 50.0, 0.0
    buzzer_holder = (
        Manifold.cylinder(10.5, 8.2, 8.2, 48)
        - Manifold.cylinder(9.0, 6.2, 6.2, 48).translate((0.0, 0.0, 2.0))
        - Manifold.cylinder(12.0, 4.5, 4.5, 36)
        - Manifold.cube((18.0, 6.0, 12.0), True).translate((-5.0, 0.0, 6.0))  # C-clip wire slot facing center
    ).translate((buz_x, buz_y, 2.8))

    # ── (D) FRONT & REAR SOCKETS: 2× 5MM LED FRICTION HOLDERS (X = +1.0, Y = ±16.5) ──
    led_holders = Manifold()
    for ly in [-16.5, 16.5]:
        lh = (
            Manifold.cylinder(11.0, 4.4, 4.4, 36)
            - Manifold.cylinder(9.5, 2.65, 2.65, 36).translate((0.0, 0.0, 2.0))
            - Manifold.cylinder(12.0, 1.9, 1.9, 24)
            - Manifold.cube((10.0, 3.2, 12.0), True).translate((0.0, -3.0 if ly > 0 else 3.0, 6.0))
        ).translate((1.0, ly, 2.8))
        led_holders = led_holders + lh

    bottom_part = bottom_part + esp_cradle + mq2_tower + buzzer_holder + led_holders

    assembled = bottom_part + top_part

    return bottom_part, top_part, assembled


def manifold_to_trimesh(m: Manifold) -> trimesh.Trimesh:
    mesh_data = m.to_mesh()
    verts = np.array(mesh_data.vert_properties)[:, :3]
    faces = np.array(mesh_data.tri_verts)
    return trimesh.Trimesh(vertices=verts, faces=faces, process=True)


if __name__ == "__main__":
    print("Building v3.1 Coaxial Glueless Modular 3D CAD enclosure meshes...")
    bot_m, top_m, asm_m = build_enclosure_parts()

    tm_bot = manifold_to_trimesh(bot_m)
    tm_top = manifold_to_trimesh(top_m)
    tm_asm = manifold_to_trimesh(asm_m)

    for name, tm in [("Bottom Base (All Cradles)", tm_bot), ("Top Shell (Lift-Off Cover)", tm_top), ("Assembled", tm_asm)]:
        print(f"  {name}: vertices={len(tm.vertices)}, faces={len(tm.faces)}, "
              f"watertight={tm.is_watertight}, bounds_mm={np.round(tm.extents, 1).tolist()}")

    hw_dir = "/home/lezgin/Desktop/Nasa_Space_Apps_Challange/FIRE-X 1.0/hardware"
    desk_dir = "/home/lezgin/Desktop/FIREX_3D_Korpus_STL"
    proto_dir = "/home/lezgin/Desktop/FIREX_3D_Korpus_STL/prototip"
    os.makedirs(hw_dir, exist_ok=True)
    os.makedirs(desk_dir, exist_ok=True)
    os.makedirs(proto_dir, exist_ok=True)

    tm_top.export(os.path.join(proto_dir, "firex-top-shell.stl"))
    tm_bot.export(os.path.join(proto_dir, "firex-bottom-base.stl"))
    tm_asm.export(os.path.join(proto_dir, "firex-assembled.stl"))

    tm_top.export(os.path.join(desk_dir, "FIREX_1_Ust_Govde_Korpus.stl"))
    tm_bot.export(os.path.join(desk_dir, "FIREX_2_Alt_Baza_ESP32_Yuvasi.stl"))
    tm_asm.export(os.path.join(desk_dir, "FIREX_Tam_Yigilmish_Korpus.stl"))

    tm_top.export(os.path.join(hw_dir, "FIREX_1_Ust_Govde_Korpus.stl"))
    tm_bot.export(os.path.join(hw_dir, "FIREX_2_Alt_Baza_ESP32_Yuvasi.stl"))
    tm_asm.export(os.path.join(hw_dir, "FIREX_Tam_Yigilmish_Korpus.stl"))
    print("All v3.1 Coaxial Glueless Modular STL files exported successfully!")
