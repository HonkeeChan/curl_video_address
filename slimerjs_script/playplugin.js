(function(t) {
    if (y.railslocked && 0 == y.page.maxh) return !0;
    t = t ? t : window.e;
    var e = y.getTarget(t);
    if (e && /INPUT|TEXTAREA|SELECT|OPTION/.test(e.nodeName)) { var n = e.getAttribute("type") || e.type || !1; if (!n || !/submit|button|cancel/i.tp) return !0 }
    if (l(e).attr("contenteditable")) return !0;
    if (y.hasfocus || y.hasmousefocus && !a || y.ispage && !a && !r) {
        var i = t.keyCode;
        if (y.railslocked && 27 != i) return y.cancelEvent(t);
        var o = t.ctrlKey || !1,
            s = t.shiftKey || !1,
            c = !1;
        switch (i) {
            case 38:
            case 63233:
                y.doScrollBy(72), c = !0;
                break;
            case 40:
            case 63235:
                y.doScrollBy(-72), c = !0;
                break;
            case 37:
            case 63232:
                y.railh && (o ? y.doScrollLeft(0) : y.doScrollLeftBy(72), c = !0);
                break;
            case 39:
            case 63234:
                y.railh && (o ? y.doScrollLeft(y.page.maxw) : y.doScrollLeftBy(-72), c = !0);
                break;
            case 33:
            case 63276:
                y.doScrollBy(y.view.h), c = !0;
                break;
            case 34:
            case 63277:
                y.doScrollBy(-y.view.h), c = !0;
                break;
            case 36:
            case 63273:
                y.railh && o ? y.doScrollPos(0, 0) : y.doScrollTo(0), c = !0;
                break;
            case 35:
            case 63275:
                y.railh && o ? y.doScrollPos(y.page.maxw, y.page.maxh) : y.doScrollTo(y.page.maxh), c = !0;
                break;
            case 32:
                y.opt.spacebarenabled && (s ? y.doScrollBy(y.view.h) : y.doScrollBy(-y.view.h), c = !0);
                break;
            case 27:
                y.zoomactive && (y.doZoom(), c = !0)
        }
        if (c) return y.cancelEvent(t)
    }
})

(function (t){t=t||B.event;var e=t.target||t.srcElement;a(e,t)})
(function (t){var e=t.ctrlKey||!1;e||(y.wheelprevented=!1)})

(function (e){d.event.simulate(t,e.target,d.event.fix(e),true)})