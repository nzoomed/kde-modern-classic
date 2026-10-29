"""KTouch, work in progress (2026-10-30): not built. The keyboard is right; the hand still needs work.
hand_d is the latest attempt, matched to the original by overlay. To try it: classicapps imports these and
sets HAND = hand_d.
"""
from gen import INK, LW, rrect


def _silver_keyboard(ic):
    """The Keyboard settings icon's keyboard in KTouch's grey and silver."""
    ic.shadow("M3,24Q3,20 7,20H57Q61,20 61,24V48Q61,52 57,52H7Q3,52 3,48Z", 2.6, 2.2)
    ic.path("M3,46H61V48Q61,52 57,52H7Q3,52 3,48Z", "#6c727a", INK, LW)
    ic.path("M3,24Q3,20 7,20H57Q61,20 61,24V46H3Z", ic.lg([(0, "#f4f5f7"), (1, "#a8adb4")]), INK, LW)
    for r in range(3):
        for k in range(8):
            x = 6.5 + r * 1.6 + k * 6.1; y = 23 + r * 5.5
            ic.path(rrect(round(x, 2), y, 5.2, 4.6, .9), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")]), "#5c6168", .6)
    ic.path(rrect(18, 40.5, 26, 4, .9), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")]), "#5c6168", .6)


def hand_c(ic):
    """C: closely traced from the original - the finger widening into the hand, a notch where it meets the
    knuckles, which bulge out to the right, and the wrist running off the lower left."""
    d = ("M26,16.2Q28.4,15 29.8,18.4Q29.6,21 28.2,23L25.4,29.6Q26.6,27.2 28.8,28.4Q31,29.8 29.8,32.4Q32.4,32 33,35Q33.6,37.8 31.6,39"
         "Q33.8,40.8 33,44Q32.6,46 31,47.6Q28.4,52.6 23.4,55.6Q19.6,57.6 16.4,57L14.4,64H4L4,49L13.6,31.6"
         "Q15.6,29.8 18,29.2Q19.6,28.2 20.2,24.6L25.4,17.6Q25.6,16.6 26,16.2Z")
    ic.shadow(d, 2, 1.7)
    ic.path(d, ic.lg([(0, "#ffecd4"), (.4, "#f4c69c"), (.75, "#d0905a"), (1, "#8a4c24")], 0, 0, 1, 0), INK, 1.2)
    ic.add('<path d="M29.8,32.4Q28,34 26.6,36.6M31.6,39Q29.6,40.4 28,43M25.4,29.8Q25,32 23.8,33.8" '
           'fill="none" stroke="#7a3c18" stroke-width=".9" stroke-linecap="round"/>')
    ic.add('<path d="M26.4,28.8Q27.6,28.2 28.6,29.2M30.6,32.8Q31.8,33 32.2,34.6M32.2,40Q32.8,41 32.6,42.4" fill="none" '
           'stroke="#ffffff" stroke-opacity=".6" stroke-width=".8" stroke-linecap="round"/>')
    ic.add('<path d="M26.8,17.8L21.8,25.4" stroke="#ffffff" stroke-opacity=".6" stroke-width=".9" stroke-linecap="round"/>')
    ic.add('<path d="M26.6,17Q28,16.2 28.8,17.8L28.2,19.6Q27.2,19 26.6,17Z" fill="#fff4ea"/>')


def hand_d(ic):
    """D: matched to the original by overlay - a slimmer finger, the hand itself below the keyboard, the
    knuckles as small bumps along its top right and the shadow on the right side rather than crease lines."""
    d = ("M26.2,17Q28,14.6 29.8,17.8L25.2,35Q26.4,33.6 28,34.4Q29.6,35.4 29.2,37.2Q31.2,37 32,39.2"
         "Q32.6,41.2 31.4,42.6Q33.4,44 33,47Q32.4,52 27,56.4Q22.6,59.6 17.4,59.8L16.4,64H4.6V48.6L10.4,35.4Q14.6,33 20.2,33.2Z")
    ic.shadow(d, 2, 1.7)
    ic.path(d, ic.lg([(0, "#ffecd4"), (.45, "#f4c69c"), (1, "#c88650")], 0, 0, 1, 0), INK, 1.2)
    ic.add('<path d="M29.2,37.2Q31.2,37 32,39.2Q32.6,41.2 31.4,42.6Q33.4,44 33,47Q32.4,52 27,56.4Q29.8,47 29.2,37.2Z" '
           'fill="#6a3010" fill-opacity=".38"/>')
    ic.add('<path d="M28.6,34.8Q27.8,36 26.8,36.6M30.6,38.2Q29.8,39.2 28.8,39.6" fill="none" stroke="#7a3c18" '
           'stroke-opacity=".7" stroke-width=".8" stroke-linecap="round"/>')
    ic.add('<path d="M26.2,35.2Q27,34.6 27.8,35M29.8,38.4Q30.8,38.6 31.2,39.6" fill="none" stroke="#ffffff" '
           'stroke-opacity=".55" stroke-width=".7" stroke-linecap="round"/>')
    ic.add('<path d="M26.9,18.6L22,31.6" stroke="#ffffff" stroke-opacity=".6" stroke-width=".8" stroke-linecap="round"/>')
    ic.add('<path d="M26.8,17.6Q28,16.4 28.9,18L28.4,19.8Q27.4,19.4 26.8,17.6Z" fill="#fff4ea"/>')


HAND = hand_d


def ktouch(ic):
    """KTouch: the silver keyboard with a hand pressing a key with its index finger."""
    ic.add('<g transform="translate(0,-15)">')
    _silver_keyboard(ic)
    ic.add("</g>")
    HAND(ic)
