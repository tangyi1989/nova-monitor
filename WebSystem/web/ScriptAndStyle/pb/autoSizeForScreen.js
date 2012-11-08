//class name "autoScreen" 会根据页面调整高度;
$(function () {
    AutoScreenHeight(".autoScreen");
})

window.onresize = function () {
    AutoScreenHeight(".autoScreen");
}
function AutoScreenHeight(className) {
    var height = GetScreenSize().Height;
    $(className).css("height", height);
}

function ScreenResize(className, minHeight, maxHeight) {
    var pos = GetScreenSize();
    if(pos.Height > maxHeight){
        $(className).css("height", maxHeight);
    }
    else if (pos.Height < minHeight) {
        $(className).css("height", minHeight);
    }
    else $(className).css("height", pos.Height);
}
function GetScreenSize()
{
    var pos = {};
    pos.Height = $(window).height();
    pos.Width = $(window).height();
    return pos;
}
