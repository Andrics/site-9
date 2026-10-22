// firefox/user.js — SITE-9 prefs (BUILD_SPEC.md §3 "Firefox").
// Firefox copies these into prefs.js at every start. Removing a line here
// doesn't undo it: reset the pref in about:config.

// Load chrome/userChrome.css and chrome/userContent.css (off by default;
// checked in Firefox 158.0.1's greprefs.js).
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// Density: standard (user's pick, round #13). In Firefox 158 (Nova) an
// unset value means "auto" (small windows switch to compact); 0 pins
// standard, 1 would pin compact.
user_pref("browser.uidensity", 0);
