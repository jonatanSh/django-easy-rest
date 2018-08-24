function Debugger(data) {

    this.data = null;
    this.underDebug = true;

    this.handle = function () {
        if (this.underDebug) {
            if ("debug_url" in this.data) {
                window.location.href = this.data['debug_url'] + "&referer=" + encodeURIComponent(window.location.href);
            }
            else {
                console.error("An error occurred (no debug url in data), in your api details:", this.data);
            }
        }
    };

    this.create = function (data) {
        this.data = data;
    }


}