
function ServerStatus()
{
    this.ObData = {
        testBt:".testBt"
    }
    this.Initial = function ()
    {
        $(this.ObData.testBt).bind("click", this, function (event) {
            event.data.PostTest();
        })
    }
    this.PostTest = function ()
    {
	/*	var postData = {};
		//postData.url = "http://218.192.168.43:9090";
        postData.data = "hell0 world";
        postData.success = function (backData)
        {
            alert(backData);
        }
        AjaxConnect(postData);     */   

		var xmlRes = new XMLHttpRequest();
        xmlRes.onreadystatechange = state_Change;
        xmlRes.open("post", "http://218.192.168.43:8080", true);
        xmlRes.send("hell0 world");

        function state_Change() {
			//alert(xmlRes.readyState);
//alert(xmlRes.responseText);
            if (xmlRes.readyState == 4) {// 4 = "loaded"
                if (xmlRes.status == 200) {// 200 = OK
                    // ...our code here...
                    alert("ok  " + xmlRes.responseText);
                }
                else {
                    alert("Problem retrieving XML data");
                }
            }
        }
    }
}
