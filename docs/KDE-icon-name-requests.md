# Icon-name requests for KDE (wishlist)

Five small wishlist items from the KDE Modern Classic icon theme. Items 1, 2, 4 and 5 have the same cause:
several places ask for one icon name, so no icon theme can tell them apart. Item 3 is an icon that
bypasses the theme altogether. They belong to different products on bugs.kde.org, so file them separately.

---

## 1. Discover: give category subcategories their own icon names

**Product:** Discover  **Component:** discover  **Severity:** wishlist

**Summary:** Let category subcategories use distinct icon names so icon themes can tell them apart

Many of Discover's category subcategories have no `<Icon>` of their own, or share one with a sibling. Icon
themes can only map icon names to pictures, so a theme cannot show different icons for subcategories that
ask for the same name. Because of that, these all look identical whatever theme is in use:

- **Games:** Action, Emulators, Puzzles, Role Playing, Sports, Launchers and Tools all fall back to
  `applications-games`; Simulation shares `applications-games-strategy` with Strategy.
- **Science:** Biology and Geology have no icon.
- **Development (as shipped by Debian):** IDEs and Profiling have no icon.

**Suggestion:** give each subcategory its own name that falls back to its parent through the normal
dash rule, for example:

```
applications-games-action        applications-games-emulators    applications-games-puzzle
applications-games-roleplaying   applications-games-sports       applications-games-simulation
applications-science-biology     applications-science-geology
applications-development-ide     applications-development-profiling
```

Because of dash fallback, `applications-games-action` resolves to `applications-games` in any theme that
doesn't draw it, so nothing changes for existing themes; themes that want to (Breeze included) can then add
distinct icons.

---

## 2. System Settings: separate icon names for Quick Settings and General Behavior

**Product:** systemsettings (or plasma-desktop, component kcms)  **Severity:** wishlist

**Summary:** Quick Settings and General Behavior both use `preferences-desktop`, so themes can't tell them apart

The Quick Settings page (`kcms/landingpage/kcm_landingpage.json`) and the General Behavior page
(`kcms/workspaceoptions/kcm_workspace.json`) in plasma-desktop both set `"Icon": "preferences-desktop"`.
They appear one after another at the top of the System Settings sidebar with the same icon, and an icon
theme has no way to give them different ones.

**Suggestion:** give each its own name that falls back to `preferences-desktop` through the dash rule, for
example:

```
preferences-desktop-quicksettings     (Quick Settings)
preferences-desktop-behavior          (General Behavior)
```

Themes that don't draw them keep showing `preferences-desktop`, exactly as today.

---

## 3. Ark: load the welcome-screen logo from the icon theme

**Product:** ark  **Severity:** wishlist

**Summary:** Welcome screen logo ignores the icon theme

Ark's welcome screen shows `aboutData.programLogo()` (`app/welcomeview/welcomeview.cpp`), and the logo is set in
`app/main.cpp` from an embedded file:

```cpp
aboutData.setProgramLogo(QIcon::fromTheme(QStringLiteral(":/ark/ark.svgz")));
```

Because that is a resource path rather than an icon name, no icon theme can replace it, so the welcome screen
always shows Breeze's Ark icon even when the taskbar, title bar and menus show the theme's. The window icon a
few lines later already does the right thing:

```cpp
application.setWindowIcon(QIcon::fromTheme(QStringLiteral("ark"), application.windowIcon()));
```

**Suggestion:** load the logo the same way, with the embedded file as the fallback:

```cpp
aboutData.setProgramLogo(QIcon::fromTheme(QStringLiteral("ark"), QIcon(QStringLiteral(":/ark/ark.svgz"))));
```

Breeze users see no change; icon themes then apply to the welcome screen too. (Small enough to send as a merge
request on invent.kde.org instead of a bug report.)

---

## 4. Discover: give the Installed page its own icon name

**Product:** Discover  **Component:** discover  **Severity:** wishlist

**Summary:** The Installed page uses `view-list-details`, the same icon as Dolphin's Details view

In `discover/qml/DiscoverWindow.qml` the Installed page is set up with:

```qml
TopLevelPageData {
    id: installedAction
    icon.name: "view-list-details"
    text: i18n("&Installed")
```

`view-list-details` is the standard name for the Details view mode (Dolphin's toolbar, file dialogs), so an icon
theme that draws it as a view-mode button also puts that button on Discover's sidebar, and cannot give the
Installed page anything better without changing every Details view button.

**Suggestion:** use a name of its own that falls back to the current one through the dash rule, for example:

```qml
icon.name: "view-list-details-installed"
```

Themes that don't draw it keep showing `view-list-details`, exactly as today; themes that want to can show an
installed-software picture there.

---

## 5. Plasma notifications: give the popup's close button its own icon name

**Product:** plasmashell  **Component:** Notifications  **Severity:** wishlist

**Summary:** The notification close button uses `window-close`, so themes can't give it a plain close mark

In `applets/notifications/components/HeadingButtons.qml` (plasma-workspace) the close button is:

```qml
PlasmaComponents3.ToolButton {
    id: closeButton
    icon.name: "window-close"
```

`window-close` is also the standard icon for "Close" / "Close Window" in application menus and toolbars. Breeze
draws it as a plain ✕, which suits both places, but themes that draw a small window with a close mark (as KDE 3's
icons did) end up putting a window picture on every notification, and can't change the popup without changing
every app's Close Window action. The Minimize/Restore button next to it (`window-minimize` / `window-restore`) has
the same issue.

**Suggestion:** use names of their own that fall back to the current ones through the dash rule, for example:

```qml
icon.name: "window-close-notification"        // falls back to window-close
icon.name: "window-minimize-notification"     // falls back to window-minimize
icon.name: "window-restore-notification"      // falls back to window-restore
```

Themes that don't draw them keep showing exactly what they show today.

---

*Reported by the author of the KDE Modern Classic icon theme (store.kde.org), who found these while
checking that every icon Plasma asks for is covered.*
