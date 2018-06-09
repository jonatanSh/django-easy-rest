// injects for disabling debugging
function DummyDebugger() {

}

Debugger = typeof(Debugger) !== "undefined" ? Debugger : DummyDebugger;
let debugHandler = new Debugger();
const REQUEST_TYPES = {
    post: "POST",
    get: "GET",
};

function RequestHandler(url) {
    this.url = url;
    /**
     * on failure returns {"error":"error value"}
     * @return {object}
     */
    this.sendSync = function (data) {
        return this.baseSync(data, REQUEST_TYPES.post);
    };

    this.getSync = function (data) {
        return this.baseSync(data, REQUEST_TYPES.get);
    };

    // legacy
    this["SendSync"] = this.sendSync;
    this["GetSync"] = this.getSync;

    this.baseSync = function (data, requestType) {
        let ajax_response = undefined;
        $.ajax(
            {
                async: false,
                url: this.url,
                type: requestType,
                data: data,
                headers: {"X-CSRFToken": getCsrf()},

                success: function (jsonResponse) {
                    ajax_response = jsonResponse;


                },
                error: function (error) {
                    debugHandler.create(error.responseJSON);
                    debugHandler.handle();
                    ajax_response = {"error": error}

                }
            });
        return ajax_response;
    };


    this.sendASync = function (data, onSuccess, onError = function (error) {
    }, additionalSuccessData = {}) {
        return this.baseASync(data, onSuccess, onError, additionalSuccessData, REQUEST_TYPES.post);
    };

    this.getASync = function (data, onSuccess, onError = function (error) {
    }, additionalSuccessData = {}) {
        return this.baseASync(data, onSuccess, onError, additionalSuccessData, REQUEST_TYPES.get);
    };

    // legacy
    this["SendAsync"] = this.sendASync;
    this["GetAsync"] = this.getASync;


    this.baseASync = function (data, onSuccess, onError, additionalSuccessData, requestType) {
        let onErrorWrapper = function (error) {
            debugHandler.create(error.responseJSON);
            debugHandler.handle();
            onError(error);
        };
        $.ajax(
            {
                async: true,
                url: this.url,
                type: requestType,
                data: data,
                headers: {"X-CSRFToken": getCsrf()},

                success: function (data) {
                    let functionData = data;
                    try {
                        functionData = JSON.parse(functionData);
                    }
                    catch (err) {

                    }
                    for (let key in additionalSuccessData) {
                        functionData[key] = additionalSuccessData[key];
                    }
                    onSuccess(functionData);
                },
                error: onErrorWrapper
            });

    };
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCsrf() {
    return getCookie("csrftoken")
}