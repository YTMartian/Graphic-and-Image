(function ($) {
    let printAreaCount = 0;
    $.fn.printArea = function () {
        let ele = $(this);
        let idPrefix = "printArea_";
        removePrintArea(idPrefix + printAreaCount);
        printAreaCount++;
        let iframeId = idPrefix + printAreaCount;
        let iframeStyle = 'width:0px;height:0px;';
        iframe = document.createElement('IFRAME');
        $(iframe).attr({
            style: iframeStyle,
            id: iframeId
        });
        document.body.appendChild(iframe);
        let doc = iframe.contentWindow.document;
        $(document).find("link").filter(function () {
            return $(this).attr("rel").toLowerCase() === "stylesheet";
        }).each(
            function () {
                doc.write('<link type="text/css" rel="stylesheet" href="'
                    + $(this).attr("href") + '" >');
            });
        doc.write('<div class="' + $(ele).attr("class") + '">' + $(ele).html()
            + '</div>');
        doc.close();
        let frameWindow = iframe.contentWindow;
        frameWindow.close();
        frameWindow.focus();
        frameWindow.print();
    };
    let removePrintArea = function (id) {
        $("iframe#" + id).remove();
    };
})(jQuery);