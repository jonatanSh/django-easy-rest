function RestConsts() {
    // here are all the rest consts before initialization

    this.API_PATH = window.location.pathname;
    this.REQUEST_TYPES = {
        post: "POST",
        get: "GET",
    };
    this.CONTEXT = null;

    this.on = function (eventName, callback) {
        if (eventName in this) {
            this[eventName](callback);
        }

    };

    this.load = function (callback) {
        $(document).ready(callback);
    };

    this.addConst = function (constName, value) {
        this[constName] = value;
    };

    this.all = function () {
        let names = [];
        for (let name of Object.getOwnPropertyNames(this)) {
            if (![
                    "on",
                    "load",
                    "addConst",
                    "all"
                ].includes(name)) {
                names.push(name);
            }
        }
        return names;
    };

}

// yes it's kind of funny but the rest consts are dynamic,
// doesn't cpp brought const_cast<> ? (:
if (!("restConsts" in window)) {
    window.restConsts = new RestConsts();
}

