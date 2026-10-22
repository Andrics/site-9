// sddm/site-9/Main.qml — SITE-9 login screen (BUILD_SPEC.md §3 "Login
// screen", Phase 5.1). SDDM 0.21.0, Qt6 greeter (sddm-greeter-qt6).
//
// P1 "access terminal": one raised VOX panel on the facility wall.
// P2: a DOS-style full-screen prompt on --field. Picked in theme.conf.
//
// Rules (§2/§3): tokens only; 1px bevels drawn as separate edge
// rectangles; radius 0; every position a whole pixel; DepartureMono
// 11px with antialiasing off (native rendering — the per-user fontconfig
// rule doesn't reach the sddm user); no animations; the text cursor is
// drawn here and never blinks; the clock redraws once a minute.
//
// From SDDM: sddm (login, reboot, powerOff, canReboot, canPowerOff,
// loginFailed), userModel, sessionModel, keyboard (capsLock), config
// (theme.conf).

import QtQuick

Rectangle {
    id: root

    // --- tokens (BUILD_SPEC.md §3) -------------------------------------
    readonly property color panel: "#445435"
    readonly property color fieldColor: "#303f25"
    readonly property color bevelLight: "#667359"
    readonly property color bevelDark: "#1f2719"
    readonly property color textColor: "#cbcfc8"
    readonly property color textBright: "#ffffff"
    readonly property color warning: "#e6a84f"
    readonly property color critical: "#ff7a5c"
    readonly property string fontFamily: "DepartureMono Nerd Font"
    readonly property int charW: 7    // DepartureMono advance at 11px
    readonly property int lineH: 14

    // --- settings (theme.conf) -----------------------------------------
    readonly property bool p2: config.variant === "P2"
    readonly property string mask: config.maskChar ? config.maskChar : "*"
    readonly property bool showSession: String(config.showSession) === "true"
    readonly property string preview: config.previewState ? config.previewState : ""

    // --- state ----------------------------------------------------------
    property bool denied: preview === "denied"
    readonly property bool caps: keyboard.capsLock || preview === "caps"
    readonly property string status: caps ? "CAPS LOCK ON"
                                    : denied ? "ACCESS DENIED" : "AWAITING CREDENTIALS"
    readonly property color statusColor: caps ? warning : denied ? critical : textColor
    property int sessionIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
    property string clock: Qt.formatTime(new Date(), "HH:mm")
    property bool enterDown: false
    readonly property string defaultUser: userModel.lastUser ? userModel.lastUser
                                        : (users.count > 0 ? users.itemAt(0).uname : "")

    color: fieldColor

    // sessions.count in the call keeps bindings live while the list fills
    function sessionName(i, count) {
        var it = sessions.itemAt(i)
        return it ? it.sname : ""
    }
    function cycleSession(step) {
        if (sessions.count > 0)
            sessionIndex = (sessionIndex + step + sessions.count) % sessions.count
    }
    function login(user, pass) {
        denied = false
        sddm.login(user, pass, sessionIndex)
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.denied = true
            p1Pass.input.text = ""
            p2Pass.text = ""
            root.focusPassword()
        }
    }
    function focusPassword() {
        if (root.p2) p2Pass.forceActiveFocus(); else p1Pass.input.forceActiveFocus()
    }
    Component.onCompleted: focusPassword()

    // Names from the models (roles: userModel name, sessionModel name).
    Repeater { id: users; model: userModel; delegate: Item { property string uname: model.name } }
    Repeater { id: sessions; model: sessionModel; delegate: Item { property string sname: model.name } }

    // Clock: wakes once a minute, on the minute. Nothing else ticks.
    Timer {
        id: tick
        running: true
        repeat: false
        interval: 60000 - (new Date().getSeconds() * 1000 + new Date().getMilliseconds())
        onTriggered: {
            var now = new Date()
            root.clock = Qt.formatTime(now, "HH:mm")
            interval = 60000 - (now.getSeconds() * 1000 + now.getMilliseconds())
            start()
        }
    }

    // --- building blocks ------------------------------------------------
    // Text: native rendering, no antialiasing, 14px line.
    component T: Text {
        font.family: root.fontFamily
        font.pixelSize: 11
        renderType: Text.NativeRendering
        antialiasing: false
        color: root.textColor
        height: root.lineH
        verticalAlignment: Text.AlignVCenter
    }

    // 1px bevel: raised = light top/left, dark bottom/right.
    component Bevel: Item {
        property bool raised: true
        anchors.fill: parent
        Rectangle { x: 0; y: 0; width: parent.width; height: 1; color: raised ? root.bevelLight : root.bevelDark }
        Rectangle { x: 0; y: 0; width: 1; height: parent.height; color: raised ? root.bevelLight : root.bevelDark }
        Rectangle { x: 0; y: parent.height - 1; width: parent.width; height: 1; color: raised ? root.bevelDark : root.bevelLight }
        Rectangle { x: parent.width - 1; y: 0; width: 1; height: parent.height; color: raised ? root.bevelDark : root.bevelLight }
    }

    // A seam: dark line over light line.
    component Seam: Item {
        height: 2
        Rectangle { x: 0; y: 0; width: parent.width; height: 1; color: root.bevelDark }
        Rectangle { x: 0; y: 1; width: parent.width; height: 1; color: root.bevelLight }
    }

    // Text input. Qt 6.12's TextInput ignores antialiasing: false, so it
    // only handles typing (its own glyphs transparent) and a crisp Text on
    // top shows what it holds. Qt's cursor blinks, so it's kept off and a
    // static one is drawn here.
    component Input: TextInput {
        id: ti
        property bool masked: false
        font.family: root.fontFamily
        font.pixelSize: 11
        color: "transparent"
        selectionColor: "transparent"
        selectedTextColor: "transparent"
        height: root.lineH
        verticalAlignment: TextInput.AlignVCenter
        echoMode: masked ? TextInput.Password : TextInput.Normal
        passwordCharacter: root.mask
        passwordMaskDelay: 0
        cursorDelegate: Item {}
        onCursorVisibleChanged: if (cursorVisible) cursorVisible = false
        Item {
            anchors.fill: parent
            clip: true
            T {
                id: shown
                // keep the end (and the cursor) in view when the text is long
                x: Math.min(0, ti.width - root.charW - implicitWidth)
                y: 0
                text: ti.displayText
                font.capitalization: ti.font.capitalization
                color: ti.activeFocus ? root.textBright : root.textColor
            }
            Rectangle {
                visible: ti.activeFocus
                x: shown.x + ti.cursorPosition * root.charW
                y: 0
                width: root.p2 ? root.charW : 1
                height: root.lineH
                color: root.textBright
            }
        }
    }

    // Raised button; pressed in while held.
    component Btn: Rectangle {
        id: b
        property string label
        property bool held: false
        signal activated()
        readonly property bool down: ma.pressed || held
        width: label.length * root.charW + 16
        height: 22
        color: down ? root.fieldColor : root.panel
        Bevel { raised: !b.down }
        T {
            x: 8
            y: 4
            text: b.label
            color: b.down ? root.textBright : root.textColor
        }
        MouseArea { id: ma; anchors.fill: parent; onClicked: b.activated() }
    }

    // ===================================================================
    // P1 — access terminal
    // ===================================================================
    Image {
        visible: !root.p2
        anchors.fill: parent
        source: config.background ? config.background : ""
        fillMode: Image.PreserveAspectCrop
        smooth: false
        asynchronous: false
    }

    Item {
        id: p1view
        visible: !root.p2
        readonly property int w: 416
        readonly property int fieldX: 128
        readonly property int rowSession: 112
        readonly property int rowStatus: root.showSession ? 142 : 112
        readonly property int rowBottom: rowStatus + 46
        readonly property int h: rowBottom + 22 + 16
        x: Math.floor((root.width - w) / 2)
        y: Math.floor((root.height - h) / 2)
        width: w
        height: h

        // sits on the wall: a dark line around the panel
        Rectangle { x: -1; y: -1; width: p1view.w + 2; height: p1view.h + 2; color: root.bevelDark }
        Rectangle { anchors.fill: parent; color: root.panel; Bevel { raised: true } }

        T { x: 16; y: 16; text: "SITE-9 // PERSONNEL ACCESS"; color: root.textBright }
        Seam { x: 12; y: 38; width: p1view.w - 24 }

        T { x: 16; y: 56; text: "OPERATOR" }
        Rectangle {
            id: p1UserBox
            x: p1view.fieldX; y: 52; width: p1view.w - p1view.fieldX - 16; height: 22
            color: root.fieldColor
            Bevel { raised: false }
            Input {
                id: p1User
                x: 6; y: 4; width: parent.width - 12
                text: root.defaultUser
                font.capitalization: Font.AllUppercase
                KeyNavigation.tab: p1Pass.input
                Keys.onReturnPressed: p1Pass.input.forceActiveFocus()
                Keys.onEnterPressed: p1Pass.input.forceActiveFocus()
            }
        }

        T { x: 16; y: 86; text: "PASSPHRASE" }
        Rectangle {
            id: p1Pass
            property alias input: p1PassInput
            x: p1view.fieldX; y: 82; width: p1view.w - p1view.fieldX - 16; height: 22
            color: root.fieldColor
            Bevel { raised: false }
            Input {
                id: p1PassInput
                x: 6; y: 4; width: parent.width - 12
                masked: true
                KeyNavigation.backtab: p1User
                onTextChanged: if (text.length > 0) root.denied = (root.preview === "denied")
                // Enter presses AUTHORIZE in while held, logs in on release.
                // Keys handlers accept every key by default: pass the rest on.
                Keys.onPressed: function (event) {
                    var enter = event.key === Qt.Key_Return || event.key === Qt.Key_Enter
                    if (enter && !event.isAutoRepeat)
                        root.enterDown = true
                    event.accepted = enter
                }
                Keys.onReleased: function (event) {
                    var enter = event.key === Qt.Key_Return || event.key === Qt.Key_Enter
                    if (enter && !event.isAutoRepeat && root.enterDown) {
                        root.enterDown = false
                        root.login(p1User.text, p1PassInput.text)
                    }
                    event.accepted = enter
                }
            }
        }

        // Session row (theme.conf showSession): ◄ name ►, click the arrows.
        T { visible: root.showSession; x: 16; y: p1view.rowSession + 4; text: "SESSION" }
        Rectangle {
            visible: root.showSession
            x: p1view.fieldX; y: p1view.rowSession; width: p1view.w - p1view.fieldX - 16; height: 22
            color: root.fieldColor
            Bevel { raised: false }
            T { x: 6; y: 4; text: "◄" }
            T { x: 20; y: 4; width: parent.width - 40; text: root.sessionName(root.sessionIndex, sessions.count); elide: Text.ElideRight }
            T { x: parent.width - 13; y: 4; text: "►" }
            MouseArea { x: 0; y: 0; width: 20; height: 22; onClicked: root.cycleSession(-1) }
            MouseArea { x: parent.width - 20; y: 0; width: 20; height: 22; onClicked: root.cycleSession(1) }
        }

        T { x: 16; y: p1view.rowStatus + 4; text: root.status; color: root.statusColor }
        Btn {
            id: authorize
            x: p1view.w - 16 - width; y: p1view.rowStatus
            label: "AUTHORIZE"
            held: root.enterDown
            onActivated: root.login(p1User.text, p1PassInput.text)
        }

        Seam { x: 12; y: p1view.rowStatus + 34; width: p1view.w - 24 }

        T { x: 16; y: p1view.rowBottom + 4; text: root.clock }
        Btn {
            id: shutdown
            visible: sddm.canPowerOff || root.preview !== ""
            x: p1view.w - 16 - width; y: p1view.rowBottom
            label: "SHUT DOWN"
            onActivated: sddm.powerOff()
        }
        Btn {
            visible: sddm.canReboot || root.preview !== ""
            x: shutdown.x - 6 - width; y: p1view.rowBottom
            label: "RESTART"
            onActivated: sddm.reboot()
        }
    }

    // ===================================================================
    // P2 — DOS-style full-screen prompt on --field
    // ===================================================================
    Item {
        id: p2view
        visible: root.p2
        anchors.fill: parent
        readonly property int mx: 44
        readonly property int my: 44
        readonly property int valueX: mx + 14 * root.charW   // after "OPERATOR....: "

        T { x: p2view.mx; y: p2view.my; text: "SITE-9 RESEARCH FACILITY // PERSONNEL ACCESS TERMINAL"; color: root.textBright }
        T { x: p2view.mx; y: p2view.my + root.lineH; text: "═".repeat(52) }
        T { x: root.width - p2view.mx - 5 * root.charW; y: p2view.my; text: root.clock }

        T { x: p2view.mx; y: p2view.my + 3 * root.lineH; text: "OPERATOR....:" }
        Input {
            id: p2User
            x: p2view.valueX; y: p2view.my + 3 * root.lineH; width: 40 * root.charW
            text: root.defaultUser
            font.capitalization: Font.AllUppercase
            KeyNavigation.tab: p2Pass
            Keys.onReturnPressed: p2Pass.forceActiveFocus()
            Keys.onEnterPressed: p2Pass.forceActiveFocus()
        }
        T { x: p2view.mx; y: p2view.my + 4 * root.lineH; text: "PASSPHRASE..:" }
        Input {
            id: p2Pass
            x: p2view.valueX; y: p2view.my + 4 * root.lineH; width: 40 * root.charW
            masked: true
            KeyNavigation.backtab: p2User
            onTextChanged: if (text.length > 0) root.denied = (root.preview === "denied")
            Keys.onReturnPressed: root.login(p2User.text, p2Pass.text)
            Keys.onEnterPressed: root.login(p2User.text, p2Pass.text)
        }
        T { visible: root.showSession; x: p2view.mx; y: p2view.my + 5 * root.lineH; text: "SESSION.....:" }
        T {
            visible: root.showSession
            x: p2view.valueX; y: p2view.my + 5 * root.lineH
            text: "◄ " + root.sessionName(root.sessionIndex, sessions.count) + " ►"
            MouseArea { anchors.fill: parent; onClicked: root.cycleSession(1) }
        }

        T { x: p2view.mx; y: p2view.my + 7 * root.lineH; text: "STATUS......:" }
        T { x: p2view.valueX; y: p2view.my + 7 * root.lineH; text: root.status; color: root.statusColor }

        T {
            id: p2Auth
            x: p2view.mx; y: p2view.my + 9 * root.lineH
            text: "[ENTER] AUTHORIZE"
            MouseArea { anchors.fill: parent; onClicked: root.login(p2User.text, p2Pass.text) }
        }
        T {
            id: p2Restart
            visible: sddm.canReboot || root.preview !== ""
            x: p2view.mx + 22 * root.charW; y: p2Auth.y
            text: "[RESTART]"
            MouseArea { anchors.fill: parent; onClicked: sddm.reboot() }
        }
        T {
            visible: sddm.canPowerOff || root.preview !== ""
            x: p2view.mx + 34 * root.charW; y: p2Auth.y
            text: "[SHUT DOWN]"
            MouseArea { anchors.fill: parent; onClicked: sddm.powerOff() }
        }
    }
}
