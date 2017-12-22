window.contextUpdateInterval = 3000;

function RestFetch(){

    this.api = new RequestHandler(window.location.pathname);

    this.fetchIntervalId = null;

    this.beforeFormatHtml = {};


    this.stopFetch = function(){
        return clearInterval(this.fetchIntervalId);
    }

    this.fetch = function(){

        currentPageContextFetcher.api.SendAsync({"action":"fetch-content"}, currentPageContextFetcher.formatData);

    };

    this.formatData = function(context){
        context = JSON.parse(context);
        $(".fetch-context").each(function(){
            let element = $(this);
            let elementId = element.attr("id");
            if(elementId === undefined){
                elementId = randomId();
                element.attr("id", elementId);
            }
            if(! (elementId in currentPageContextFetcher.beforeFormatHtml))
                currentPageContextFetcher.beforeFormatHtml[elementId] = element.html();

            let html = "";
            html = currentPageContextFetcher.beforeFormatHtml[elementId];
            for(key in context){

                html = html.replace("{"+key+"}", context[key]);
            }

            element.html(html);

        })
    };

    this.bind = function(){

        setInterval(this.fetch, window.contextUpdateInterval);
    }


}

var currentPageContextFetcher = new RestFetch();

$(document).ready(function(){

    // this script will bind only for pages with the fetch context class
    if($(".fetch-context").length > 0)
    {
        // first fetch
        currentPageContextFetcher.fetch();

        // always fetch
        currentPageContextFetcher.bind();
    }

});

function randomId() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4()  + s4() + s4() +
    s4() +  s4() + s4() + s4();
}


