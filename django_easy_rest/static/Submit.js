let post_location = window.location.href;

if (!post_location.endsWith("/"))
    post_location = post_location += "/";
let handler = new RequestHandler(post_location);

function handle_errors(element_id, message) {
    $("#error_handler_post" + element_id).remove();
    $("#id_" + element_id).before("<p id='error_handler_post" + element_id + "' style='color:red'>" + message + "</p>")
}

let afterPost = function (data) {
    if (typeof (data) === "string") {
        try {
            data = JSON.parse(data);

        }
        catch (err) {
            return;
        }
    }
    if ('status' in data) {
        if (data.status === "post-failure")
            PostError(data);
        else
            postSuccess(data);
    }
};

var postSuccess = function (data) {
};

var PostError = function (data) {
    if ("form_errors" in data) {
        let errors = data.form_errors;
        if (typeof(errors) === "object") {
            for (let key in errors) {
                handle_errors(key, errors[key]);
            }
        }
    }
};

function easyRestSubmit(event) {
    event.preventDefault();
    handler.SendAsync($(event.target).serialize(), afterPost, afterPost);

}