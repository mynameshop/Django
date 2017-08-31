var AjaxHelper = {
    getXmlHttpReq: function () {
        if (window.XMLHttpRequest) {
            return new XMLHttpRequest();
        } else {
            // IE6 and IE5 fallback
            return new ActiveXObject("Microsoft.XMLHTTP");
        }
    },
    commence: function (url, method, onSuccess, onError, requestData) {
        var xhttp = AjaxHelper.getXmlHttpReq();
        if (!method) {
            method = 'GET';
        }
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState === 4) {
                if (xhttp.status === 200) {
                    onSuccess(xhttp.responseText);
                } else {
                    onError(xhttp.responseText);
                }
            }
        };

        xhttp.open(method, url, true);
        if(requestData) {
            xhttp.send(requestData);
        } else {
            xhttp.send();
        }
        

    }
};

