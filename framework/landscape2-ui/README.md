# Landscape2 native Research route

The Research page is a small extension of the pinned Landscape2 web application,
not a parallel site. It reuses the upstream Solid Router, Header, MobileDropdown,
Guide table of contents, content typography, responsive sidebar, and Footer.

`REVISION` pins the upstream source used for the compiled UI bundle. The source
overlay lives in `research/`, and `scripts/patch-landscape2-ui.py` applies the
route and navigation changes with exact-match guards so upstream changes fail
clearly instead of producing a silently incompatible bundle.
