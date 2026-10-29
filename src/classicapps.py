"""KDE Classic Vector: current KDE apps redrawn from their KDE Classic (KDE 3) originals, or a KDE 3
predecessor's icon (docs/kde-apps-redraw-list.md lists the sources). Imported by apps2, which adds the names.
"""
from gen import Icon, INK, LW, circle, rrect
from uitrace import _pencil
WOOD = ("#f0b070", "#b8662a", "#5a2806")
CHALK = "#f4f4ec"


def okteta(ic, hs=.76, depth=1.3):
    """Okteta (after KDE 3's KHexEdit): a clipboard of ruled paper with a chrome H tilted to match the
    orange pencil beside it."""
    sheet = "M3,9H51V61H3Z"
    ic.shadow(sheet, 2.4, 2)
    ic.path(sheet, ic.lg([(0, "#ffffff"), (.6, "#fffdf0"), (1, "#ece4c4")], 0, 0, 1, 1), INK, LW)
    for k in range(7):
        ic.add(f'<path d="M7,{19 + k * 6}H47" stroke="#9aa2ec" stroke-width="1.2"/>')
    # the clip
    ic.path("M18,10V6Q18,3 21,3H33Q36,3 36,6V10Q36,13 33,13H21Q18,13 18,10Z",
            ic.lg([(0, "#f0f0ff"), (.5, "#b8bce8"), (1, "#5a5e98")]), INK, 1.3)
    ic.add('<path d="M23,7H31" stroke="#5a5e98" stroke-width="1.6" stroke-linecap="round"/>')
    # chrome block H, leaning at the pencil's angle, with a shallow edge for depth
    H = "M0,0H6V8H14V0H20V22H14V13H6V22H0Z"
    ic.add(f'<g transform="translate(22,36) rotate(-53) scale({hs}) translate(-10,-11)">')
    ic.add(f'<path d="{H}" fill="#3c4148" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round" '
           f'transform="translate({depth},{depth})"/>')
    ic.path(H, ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (.55, "#7b818a"), (1, "#e4e6e9")], 0, 0, .3, 1), INK, 1.3 / hs)
    ic.add("</g>")
    _pencil(ic, "translate(57,19) rotate(37) scale(.85) translate(-6,0)")


def _board(ic):
    """KMathTool's square chalkboard: bright green slate in a wooden frame."""
    f = "M5,5H59V59H5Z"
    ic.shadow(f, 2.6, 2.2)
    ic.path(f, ic.lg([(0, WOOD[0]), (.5, WOOD[1]), (1, WOOD[2])], 0, 0, 1, 1), INK, LW)
    ic.path("M10,10H54V54H10Z", ic.lg([(0, "#5ad05a"), (.5, "#2aa83a"), (1, "#127a22")], 0, 0, 1, 1), INK, 1.1)
    ic.add('<path d="M11,11H53" stroke="#ffffff" stroke-opacity=".25" stroke-width="1.2"/>')


def _chalk(ic, d, w=2.3):
    ic.add(f'<path d="{d}" fill="none" stroke="{CHALK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".95"/>')


# x² + y, chalked across the top of the board
ALGEBRA = ("M14,16L21,26M21,16L14,26"                       # x
           "M23,13.4Q25,11 27,12.6Q28,14.4 23.4,18H28"      # ²
           "M31,21H38M34.5,17.5V24.5"                        # +
           "M41,16L45,23M49,16L42,30")                       # y


def _wrench(ic, s=.92):
    """KMathTool's spanner: handle to the lower left, open jaw to the upper right."""
    ic.add(f'<g transform="translate(35,41) rotate(45) scale({s}) translate(-36,-38)">')
    d = ("M32.8,11.06V20H39.2V11.06A9.5,9.5 0 0 1 40,28.62V56Q36,61 32,56V28.62A9.5,9.5 0 0 1 32.8,11.06Z")
    ic.shadow(d, 2, 1.7)
    ic.path(d, ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (1, "#4c5158")], 0, 0, 1, 0), INK, 1.3 / s)
    ic.add('<path d="M34.6,31V54" stroke="#ffffff" stroke-opacity=".6" stroke-width="1.2"/>')
    ic.add("</g>")


def kalgebra(ic):
    """KAlgebra: KMathTool's chalkboard and spanner, with x² + y chalked on it in place of 2 + 3."""
    _board(ic)
    ic.add('<g transform="translate(1,0) scale(.86)">'); _chalk(ic, ALGEBRA, 2.6); ic.add("</g>")
    _wrench(ic)


CLASSIC_APPS = {"okteta": okteta, "kalgebra": kalgebra}
CLASSIC_ALIASES = {"org.kde.okteta": "apps/okteta", "org.kde.kalgebra": "apps/kalgebra",
                   # Kamoso (webcam): KDE 3's camera is the theme's camera, as for camera-web
                   "kamoso": "camera-photo", "org.kde.kamoso": "camera-photo"}
