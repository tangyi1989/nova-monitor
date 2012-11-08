//json convert to string
var Convert = {
    toJSONString: function (obj) {
        switch (typeof (obj)) {
            case "object":
                var result = [];
                if (obj instanceof Array) {
                    for (var i = 0, len = obj.length; i < len; i++) {
                        result.push(Convert.toJSONString(obj[i]));
                    }
                    return "[" + result.toString(",") + "]";
                } else if (obj instanceof RegExp) {
                    return obj.toString();
                } else {
                    for (var attribute in obj) {
                        result.push("\"" + attribute + "\"" + ":" + Convert.toJSONString(obj[attribute]));
                    }
                    return "{" + result.join(",") + "}";
                }
            case "function":
                return "function() {}";
            case "number":
                return obj.toString();
            case "string":
                return "\"" +
                        obj.replace(/(\\|\")/g, "\\$1")
                            .replace(/\n|\r|\t/g,
                                    function (a) {
                                        return ("\n" == a) ? "\\n" :
                                                ("\r" == a) ? "\\r" :
                                                ("\t" == a) ? "\\t" : "";
                                    }
                        ) +
                        "\"";
            case "boolean":
                return obj.toString();
            default:
                return obj.toString();
        }
    },
    ToStringJSON: function (content) {//json convert to string
        return eval("(" + content + ")");
    }
};

function PostAjax(postContent) {
    $.ajax({
        url: postContent.url,
        type: postContent.type,
        data: Convert.toJSONString(postContent.data),
        error: postContent.error,
        complete: postContent.complete,
        beforeSend: postContent.beforeSend,
        timeout: postContent.timeout,
        dataType: postContent.dataType,
        async: postContent.async,
        cache: postContent.cache,
        contentType: postContent.contentType,
        gobal: postContent.gobal,
        success: function (backdata, strStatus, strObject) {			
            //alert(backdata);
            if (backdata.Status != undefined) {
                if (backdata.Status.toLowerCase() == "redirect") {
                    window.location.replace(backdata.BackPack);
                    return;
                }
            }
            postContent.success(backdata, strStatus, strObject);
            //if (console.clear != undefined) console.clear();
            //console.clear();
        }
    });
}
function SetDefaultAjax(postData) {
    var defaultData = {
        url: "",
        type: "post",
        timeout: 10000,
        dataType: "json",
        async: true,
        cache: false,
        gobal: false,
        contentType: "application/x-www-form-urlencoded",
        error: function (backdata, strStatus)
        {
            console.log(backdata + "" + strStatus + "     error");
        },
        success: function (backdata, strStatus, strObject)
        {
          //  alert(Convert.toJSONString(backdata) + "    success");
        },
        complete: function (XMLHttpRequestObj, strStatus)
        {
            //alert(strStatus + "  Complete");
            //console.clear();
        },
        beforeSend: function (XMLHttpRequestObj)
        {
            //alert(XMLHttpRequestObj + "   beforSend");
        }
    };
    if (postData == undefined && postData != {})
        return defaultData;
    if (postData.url != undefined && postData.url != "") {
        defaultData.url = postData.url;
    }
    if (postData.type == "post" || postData.type == "get") {
        defaultData.type = postData.type;
    }
    if (postData.data == undefined) {
        defaultData.data = "";
    }
    else
        defaultData.data = postData.data;
    if (postData.timeout != undefined) {
        if (typeof (postData.timeout) == "number") {
            if (postData.timeout >= 600)
                defaultData.timeout = postData.timeout;
        }
    }
    if (postData.contentType != undefined) {
        defaultData.contentType = postData.contentType;
    }
    if (postData.dataType != undefined) {
        var str = "html,script,text,json,xml";
        if (str.search(postData.dataType) != -1) {
            defaultData.dataType = postData.dataType;
        }
    }
    if (postData.async != undefined) {
        //alert(typeof (postData.async));
        if (typeof (postData.async) == "boolean")
            defaultData.async = postData.async;
    }
    if (postData.cache != undefined)
        if (typeof (postData.cache) == "boolean")
            defaultData.cache = postData.cache;
    if (postData.gobal != undefined)
        if (typeof (postData.gobal) == "boolean")
            defaultData.gobal = postData.gobal;
    if (postData.error != undefined)
    //alert(typeof(postData.error));
        if (typeof (postData.error) == "function")
            defaultData.error = postData.error;
    if (postData.success != undefined)
        if (typeof (postData.success) == "function")
            defaultData.success = postData.success;
    if (postData.complete != undefined)
        if (typeof (postData.complete) == "function")
            defaultData.complete = postData.complete;
    if (postData.beforeSend != undefined)
        if (typeof (postData.beforeSend) == "function")
            defaultData.beforeSend = postData.beforeSend;
    return defaultData;
}
function AjaxConnect(postJsonData) {
    var postData = SetDefaultAjax(postJsonData);
    PostAjax(postData);
}
