var page = require('webpage').create();                                         
// video url must have http:// suffix
//var videoUrl = phantom.args[0];
var videoUrl = "http://v.youku.com/v_show/id_XMTc3NDkwOTE2MA==.html?spm=a2hww.20023042.m_223465.5~5~5~5~5~5~A&from=y1.3-idx-beta-1519-23042.223465.1-1"
//var videoUrl = "click_test.html"
var videoTitle = null;
var playVideo = null;
window.setTimeout(function(){
   phantom.exit();
},  3* 60 * 60 * 1000);

//it is a timer for the same page. 
//if it redirect to other video page because this video has finish
// we will kill the browser.
window.setInterval(function(){
    if(videoTitle != null && videoTitle != page.title){
	   //console.log(videoTitle);
        phantom.exit();
    }	
}, 1000);

page.onConsoleMessage = function (msg) {
    console.log('Page console msg: ' + msg);
};

page.onResourceRequested = function (request) {
    
    //console.log('Request ' + JSON.stringify(request, undefined, 4));
};
page.onResourceReceived = function (response) {
    // if(response.url.indexOf("mp4") != -1){
    //     console.log("receive: " + response.url)
    //     //console.log('Receive ' + JSON.stringify(response, undefined, 4));
    // }
};
page.on
page.open(videoUrl , function () {
    videoTitle = page.title;
    // if(page.url.indexOf("youku.com") != -1){
    //     console.log("in youku.com");
    //     page.evaluate(function() {
    //         console.log("in evaluate function");
    //         playVideo = document.getElementById('sMain');  
    //         playVideo.click();
    //         console.log(playVideo);
    //     });
    //     console.log("in youku.com");
        
    //     //it is from youku.com
    //     //find the player div
    // }
    page.includeJs("jquery.min.js", function(){
        window.setInterval(function(){
            page.evaluate(function() {
                console.log("in evaluate function");
                var ev = document.createEvent("MouseEvent");
                ev.initMouseEvent("click", true, true, null,
                     null, null, null, null, null,
                     false, false, false, false,
                     0, null);            // charCodeArg);
                //document.querySelector("a").dispatchEvent(ev);
                document.getElementById('movie_player').dispatchEvent(ev);                    

                var ev = document.createEvent("KeyboardEvent");
                ev.initKeyEvent("keydown",       // typeArg,                                                           
                   true,             // canBubbleArg,                                                        
                   true,             // cancelableArg,                                                       
                   null,             // viewArg,  Specifies UIEvent.view. This value may be null.     
                   false,            // ctrlKeyArg,                                                               
                   false,            // altKeyArg,                                                        
                   false,            // shiftKeyArg,                                                      
                   false,            // metaKeyArg,                                                       
                    39,               // keyCodeArg,                                                      
                    0);              // charCodeArg);
                //document.querySelector("a").dispatchEvent(ev);
                document.getElementById('movie_player').dispatchEvent(ev);
                //page.sendEvent('keypress', page.event.key.Right, null, null, null);
            });
        }, 5000);
        
    });
    

    console.log("finish load");
    console.log("video title: " + videoTitle);
});



//TODO: click the right for player faster.
// window.setInterval(function(){
//     page.sendEvent('keypress', page.event.key.Space, null, null, null);
//     console.log("page key press");
// }, 10000);
