import cv2
from state import AppState


def draw_menu(frame, state: AppState):
    """Draw a translucent control panel that shows hotkeys and toggle status."""
    panel_x, panel_y = 10, 10
    panel_w, panel_h = 325, 230
    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (panel_x, panel_y),
        (panel_x + panel_w, panel_y + panel_h),
        (30, 30, 30),
        -1,
    )
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    cv2.putText(
        frame,
        "Menu",
        (panel_x + 15, panel_y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    items = [
        ("g", "Filtre gris", state.gray),
        ("h", "Chapeau", state.hat),
        ("m", "Masque", state.mask),
        ("d", "Rond qui tombe", state.drop),
        ("s", "Bulles sourire", state.smile),
        ("r", "Miroir", state.mirror),
    ]

    y = panel_y + 60
    for key, label, enabled in items:
        status_color = (0, 220, 0) if enabled else (0, 0, 220)
        status_text = "ON" if enabled else "OFF"
        cv2.putText(
            frame,
            f"{key.upper()} : {label}",
            (panel_x + 20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            2,
        )
        cv2.putText(
            frame,
            status_text,
            (panel_x + 235, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            status_color,
            2,
        )
        y += 28

    tips = [
        "Maintenez Q pour quitter",
        "Appuyez sur les lettres pour basculer les effets",
    ]
    tip_y = panel_y + panel_h - 45
    for tip in tips:
        cv2.putText(
            frame,
            tip,
            (panel_x + 15, tip_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (240, 240, 240),
            1,
        )
        tip_y += 20
