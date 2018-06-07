function Debugger(data) {

    this.data = null;
    this.underDebug = true;

    this.handle = function () {
        if (this.underDebug) {
            // validate the token here ?
            window.location.href = this.data['debug_url'] + "&referer=" + encodeURIComponent(window.location.href);
        }
    };

    this.create = function (data) {
        this.data = data;
    }


}