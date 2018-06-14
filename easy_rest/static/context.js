let init_context = function () {

    // default is current page
    let api = new RequestHandler();
    api.getASync({"action": "fetch_context"}, function (data) {
        window.restConsts.addConst("CONTEXT", data);
    });

};

// call init and destruct the stack, that's why it's inside a function
init_context();
